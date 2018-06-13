import caffe
import leveldb
import numpy as np
import sys
import pickle
from caffe.proto import caffe_pb2

#read features extracted by caffe and converted to vector...
def getFeature(featFile, featResult):
	db = leveldb.LevelDB(featFile)
	datum = caffe_pb2.Datum()
	num = 0
	featWriter = open(featResult,"w")
	dataList = []
	for key, value in db.RangeIter():	
		num += 1
		print key
		datum.ParseFromString(value)
		data = caffe.io.datum_to_array(datum)
		data = data.reshape((4096))
		tmpStr = ""
		for i in xrange(len(data)):
			tmpStr += str(round(data[i],6)) + " "
		tmpStr = tmpStr[0:-1]
		featWriter.write(tmpStr + "\n")
	featWriter.close()	
	print num
	
if __name__=="__main__":
	
	if len(sys.argv)!=3:
		print "Usage: python readFeat.py [featFile] [featResult]"
		sys.exit(0)
	featFile = sys.argv[1]
	featResult=sys.argv[2]
	getFeature(featFile, featResult)
