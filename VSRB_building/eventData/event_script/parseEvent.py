""" This script is used fro parsing image-image search result """
import sys
def parse(eventLog, result):
	
	writer = open(result, "w")
	resultList = []
	with open(eventLog, "r") as f:
		for line in f:
			line = line.strip()
			if line.startswith("for query image:"):
				pos1 = line.rfind("/")
				if pos1 == -1:
					continue
				queryId = line[pos1 + 1 : ]
				writer.write(queryId)
			elif line.startswith("image:WIKI_IMGS"):
				pos1 = line.rfind("/")
				pos2 = line.rfind("score")
				resultId = line[pos1 + 1 : pos2 - 1]
				resultList.append(resultId)
				if len(resultList) == 100:
					for rsId in resultList:
						writer.write("|" + rsId)
					writer.write("\n")
					resultList = [] 
			else:
				continue
	writer.close()


if __name__=="__main__":

	if len(sys.argv) != 3:
		print "Usage: python parseEvent.py [eventLog] [result] "
		sys.exit(0)

	eventLog = sys.argv[1]
	result = sys.argv[2]
	parse(eventLog, result)
