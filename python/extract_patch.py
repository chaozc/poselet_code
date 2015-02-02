import os
import cv2
from sys import argv
from poseletFunc import *

if __name__ == "__main__":
	#argv[1]: patch list file
	#argv[2]: output dir
	#argv[3]: output lines number
	conf = config()
	inf = open(argv[1], 'r')
	lines = inf.readlines()
	cnt = 0
	tot = len(lines)

	try:
		no = int(argv[3])
	except:
		no = tot+1
	for line in lines:
		extract_patch(line, argv[2], conf)
		cnt += 1
		print cnt, '/', tot, 'patches extracted'
		if cnt == no:
			break