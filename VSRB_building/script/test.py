import sys
import numpy as np
def cosine(qVec, aVec):
	qSum = np.sqrt(np.sum(qVec*qVec)) 
	aSum = np.sqrt(np.sum(aVec*aVec))
	return np.dot(qVec, aVec)/(qSum * aSum)
def computeSim(vecFile1, vecFile2):
	vec1, vec2 = None, None
	with open(vecFile1,'r') as f:
		for line in f:
			line = line.strip()
			parts = line.split(' ')
			vec1 = np.zeros(len(parts))
			for i in xrange(len(parts)):
				vec1[i] = parts[i]
	with open(vecFile2,'r') as f:
		for line in f:
			line = line.strip()
			parts = line.split(' ')
			vec2 = np.zeros(len(parts))
			for i in xrange(len(parts)):
				vec2[i] = parts[i]
	print cosine(vec1, vec2)

if __name__=="__main__":
	
	vecFile1 = sys.argv[1]
	vecFile2 = sys.argv[2]
	computeSim(vecFile1, vecFile2)
