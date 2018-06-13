import sys
#remove corrupted images from image lists, which can't open by caffe
def removeUnvalidImg(originFile, filterFile, logFile):
	# originFile  data/uniqPicName
	# filterFile  data/wikiTrain
	# logFile     run create_imagenet.sh  log file
	imgLists = set()
	with open(logFile, "r") as f:
		for line in f:
			line = line.strip()
			pos1 = line.find('/')
			if pos1 != -1:
				name = line[ pos1 + 1 : ] # unvlid image path
				print "remove: ", name
				imgLists.add(name)

	writer = open(filterFile, "w")
	with open(originFile, "r") as f:
		for line in f:
			line = line.strip()
			parts = line.split("|||")
			picPath = parts[1]
			if picPath not in imgLists:
				writer.write(picPath + " 0\n")
	writer.close()


if __name__=="__main__":
	
	if len(sys.argv)!=4:
		print "Usage python removeUnvalidImg.py [originFile] [filterFile] [logFile]"
		exit(0)
	originFile = sys.argv[1]
	filterFile = sys.argv[2]
	logFile = sys.argv[3]

	removeUnvalidImg(originFile, filterFile, logFile)


