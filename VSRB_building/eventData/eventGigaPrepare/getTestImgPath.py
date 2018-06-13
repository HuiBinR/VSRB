"""This script is used for acquiring the real path of images """
import sys

# imgIdFile .. contains image id, 
# projectFile ... contains image id - path - description project relation

def getRealPath(imgIdFile, projectFile, pathFile):
	imgId2Path = {}
	with open(projectFile, 'r') as f:
		for line in f:
			line = line.strip()
			parts = line.split('|||')
			imgId = parts[0]
			path = parts[1]
			imgId2Path[imgId] = path
	
	writer = open(pathFile, "w") 
	with open(imgIdFile, "r") as f:
		for line in f:
			line = line.strip()
			if not imgId2Path.has_key(line): 
				print "error, id is: ", line
				continue
			path = imgId2Path[line]
			writer.write(path + " 0\n")
	writer.close()


if __name__=="__main__":
	
	if len(sys.argv) != 4:
		print "Usage: python getTestImgPath.py [imgIdFile] [projectFile] [pathFile]"
		sys.exit(0)
	
	imgIdFile = sys.argv[1]  #image_uniq
	projectFile = sys.argv[2] #img_id2path2discrip.txt
	pathFile = sys.argv[3]   #  test image path for image-image search system
	getRealPath(imgIdFile, projectFile, pathFile)





			
