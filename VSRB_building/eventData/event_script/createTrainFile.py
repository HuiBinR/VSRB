# -*- coding=utf8 -*-
import os
import sys

def listAllFile(imgDir, testFile):
	testReader = open(testFile, "w")
	list_dirs = os.walk(imgDir)
	for root, child_dirs, files in list_dirs:
		#for d in child_dirs:
		#	print os.path.join(root, d)
		for f in files:
			testReader.write(os.path.join(root,f)+" 0\n")
	testReader.close()

if __name__=="__main__":
	
	if len(sys.argv)!=3:
		print "Usage: python createTrainFile.py [imgDir] [testFile]"
		sys.exit(0)

	imgDir = sys.argv[1]
	testFile = sys.argv[2]
	
	listAllFile(imgDir, testFile)
	
