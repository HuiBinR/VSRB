""" This script is used for splitting VSRB image data  """
import sys
def getVSRBPart(allTrainFile, vsrbPart, result):
	rowNum = 0
	id2LineNum = {}
	id2Path = {}
	with open(allTrainFile, 'r') as f:
		for line in f:
			line = line.strip()
			pos1 = line.rfind('/')
			pos2 = line.rfind(' ')
			id = line[pos1 + 1 : pos2]
			id2LineNum[id] = rowNum
			id2Path[id] = line[0: pos2]
			rowNum += 1
	
	writer = open(result , "w")
	with open(vsrbPart, 'r') as f:
		for line in f:
			line = line.strip()
			if id2LineNum.has_key(line):
				num = id2LineNum[line] 
				path = id2Path[line]
				fieldId = num / 46624  # belongs to which part...(from 0 to 15)
				trainMap = mapList[fieldId] #image path -- position in separate file..
				if trainMap.has_key(path):
					position = trainMap[path]  #position 
					writer.write(str(fieldId) + '|' + str(position) + '|' + path + "\n")
				else:
					print "error"
			else:
				print "error",line
	writer.close()	
def getSepMap(trainPartFile):
	indexList = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15']
	mapList = []
	for index in indexList:
		trainMap = {}
		with open(trainPartFile + index, 'r') as f:
			rowNum = 0
			for line in f:
				line = line.strip()
				pos = line.rfind(' ')
				path = line[0 : pos]
				trainMap[path] = rowNum
				rowNum += 1
		mapList.append(trainMap)
	return mapList

	
if __name__=="__main__":
	
	if len(sys.argv) != 4:
		print "Usage python VSRB_dataProcess.py [allTrainFile] [vsrbPart] [result]"
		sys.exit(0)
	
	allTrainFile = sys.argv[1]
	vsrbPart = sys.argv[2]
	result = sys.argv[3]

	mapList = getSepMap(allTrainFile)
	getVSRBPart(allTrainFile, vsrbPart, result)
