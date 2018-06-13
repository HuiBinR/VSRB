import sys
#remove corrupted images from image lists, which can't open by caffe
def removeUnvalidImg(originFile, filterFile, logFile):
	imgLists = set()
	with open(logFile, "r") as f:
		for line in f:
			line = line.strip()
			pos1 = line.rfind('/')
			if pos1 != -1:
				tmpline = line[0:pos1] #path without name
				pos2 = tmpline.rfind('/')
				name = "WIKI_IMGS/" + line[pos2 + 1 : ]
				print "remove: ", name
				imgLists.add(name + " 0")

	writer = open(filterFile, "w")
	with open(originFile, "r") as f:
		for line in f:
			line = line.strip()
			if line not in imgLists:
				writer.write(line + "\n")
	writer.close()


if __name__=="__main__":
	
	if len(sys.argv)!=4:
		print "Usage python removeUnvalidImg.py [originFile] [filterFile] [logFile]"
		exit(0)
	originFile = sys.argv[1]
	filterFile = sys.argv[2]
	logFile = sys.argv[3]

	removeUnvalidImg(originFile, filterFile, logFile)


