import sys
import pickle
import numpy as np
import theano
import theano.tensor as T
import gc
import leveldb
import caffe

from caffe.proto import caffe_pb2

"""
query: query image's feature vectors
queryList: query image path
allData: image  datasets feature vectors...
allDataList: image datasets path
"""
def euclidean(qVec, aVec):
	dist = np.sqrt(np.sum((qVec - aVec) * (qVec - aVec)))
	return dist

def cosine(qVec, aVec):
	qSum = np.sqrt(np.sum(qVec*qVec)) 
	aSum = np.sqrt(np.sum(aVec*aVec))
	return np.dot(qVec, aVec)/(qSum * aSum)
"""
Search similar images of query image..,according to cosine similarity of features..
queryFeat -- features extracted from query image
allDataFeat -- features of all images
"""
def Search(queryFeat, queryList, allDataList):
	
	dataSize = 745984  # image size
	batchSize = 46624  # batch size
	
	#read image's path file
	queryMap = {} #query image id -- query image path
	with open(queryList, "r") as f:
		rowNum = 0
		for line in f:
			line = line.strip()
			pos = line.rfind(' ')
			name = line[0:pos]
			queryMap[rowNum] = name
			rowNum += 1

	allDataMap = {} #all images id -- all images path
	with open(allDataList, "r") as f:
		rowNum = 0
		for line in f:
			line = line.strip()
			pos = line.rfind(' ')
			allDataMap[rowNum] = line[0:pos]
			rowNum += 1

	#read query image feature file
	queryVec = []
	row = 0
	with open(queryFeat, "r") as qfile:
		for line in qfile:
			row += 1
			line = line.strip()
			qVec = []
			tokens = line.split(' ')
			for val in tokens:
				qVec.append(float(val))
			qVec = np.array(qVec, dtype="float32")
			queryVec.append(qVec)
   	
	queryVec = np.array(queryVec, dtype="float32")
	# extra data
	queryBatchSize = 6000   #query batch size
	extraSize = queryBatchSize - queryVec.shape[0] % queryBatchSize
	extraData = queryVec[:extraSize]
	queryVec = np.append(queryVec, extraData, axis=0)
	
	basePath = "/newVolume2/yaoliang/ImageSearch/feature_extraction/train_data_valid"
	#batch search	
	for i in xrange(queryVec.shape[0]/queryBatchSize):
		partQuery = queryVec[i * queryBatchSize : (i+1) * queryBatchSize]
		partQueryVec = np.array(partQuery, dtype="float32")
		
		#we sliced wiki image data, in order to reduce the memory
		topVal, topIndices = None, None
		
		sumSize = 0
		for j in xrange(dataSize/batchSize):
			values, indices, partSize = getSim(basePath, j, partQueryVec, sumSize)
			sumSize += partSize
			if j==0:
				topVal = values
				topIndices = indices
			else:
				topVal = np.concatenate([values, topVal], axis=1)
				topIndices = np.concatenate([indices, topIndices], axis=1)
			print topVal.shape
			print topIndices.shape
		for row in xrange(topVal.shape[0]):
			rowMap = {}
			for col in xrange(topVal.shape[1]):
				index = topIndices[row][col]
				value = topVal[row][col]
				rowMap[index] = value
	
			rowSorted = sorted(rowMap.items(), key=lambda d:d[1], reverse=True)
			topResult = rowSorted[0:100]
			if row + queryBatchSize * i >= len(queryMap):
				break
			print "for query image:", queryMap[row +  queryBatchSize * i]
			
			for index, value in topResult:
				print "image:%s score:%s\n"%(allDataMap[index], value)
			print "-------------------"

#read features extracted by caffe and converted to vector...
def getFeature(featFile, index):
	
	path = "/newVolume2/yaoliang/ImageSearch/eventGigaPrepare/vsrb_data_"
	indexes = set()
	with open(path + index, 'r') as f:
		for line in f:
			line = line.strip()
			parts = line.split('|')
			index = int(parts[1]) + 1
			indexes.add(index)

	db = leveldb.LevelDB(featFile)
	print "read feature file: ", featFile
	datum = caffe_pb2.Datum()
	num = 0
	dataList = []
	for key, value in db.RangeIter():	
		num += 1
		if num not in indexes:
			continue
		datum.ParseFromString(value)
		data = caffe.io.datum_to_array(datum)
		data = data.reshape((4096))
		dataList.append(data)
	print "index:%s number:%s"%(index, num)
	return np.array(dataList, dtype="float32")

def getSim(path, index, queryVec, sumSize):
	
	topN = 100
	## load wiki image features..
	dataVec = None
	if index >= 10:
		dataVec = getFeature(path + str(index), str(index))
	else:
		dataVec = getFeature(path + "0" + str(index), "0" + str(index))	
	partSize = dataVec.shape[0]

	dataVec = np.array(dataVec, dtype="float32")
	print "dataVec: %s_%s"%(index, dataVec.shape)
	queryVec = np.array(queryVec, dtype="float32")
	print "queryVec: %s_%s"%(index, queryVec.shape)	
	#compute cosine similarity
	#threadLock.acquire()
	simArr = cosineFun(queryVec, dataVec)
	#threadLock.release()
	# release lock
	print "simArr: %s_%s"%(index, simArr.shape)	
	indices = np.argsort(simArr, axis=1) # sorted indices..
	#select topN data 
	dim0 = np.arange(simArr.shape[0]).repeat(topN)
	dim1 = indices[:,-topN:].flatten()
	values = simArr[dim0, dim1].reshape(simArr.shape[0],topN) 
	print "values: ", values
	indices += sumSize
	return values, indices[:,-topN:], partSize

if __name__=="__main__":
	
	if len(sys.argv)!=4:
		print "Usage python compute_distance.py [queryFeat] [queryList][allDataList]"
		exit(0)
	query = sys.argv[1]  #query image feature vector
	queryList = sys.argv[2] #query image path..
	allDataList= sys.argv[3] # image path of image datasets...
	
	#threadLock = threading.Lock() #share lock 

	#step1 using query images, to retrieve similar images..
	#compile theano function 
	x = T.matrix('x')
	y = T.matrix('y')
	z = T.matrix('z')
	rDot = T.dot(x, y.T)
	xNorm = T.sqrt((x ** 2).sum(1).reshape((-1,1)))
	yNorm = T.sqrt((y ** 2).sum(1).reshape((1,-1)))
	z = rDot / (xNorm * yNorm)
	cosineFun = theano.function([x,y],z)
	#search, outputs partial sorted retrieval result 
	Search(query, queryList, allDataList)
	
