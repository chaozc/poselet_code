import os
import cv2
import numpy as np
from sys import argv
from MyRandint import MyRandint
from poseletFunc import *
if __name__ == "__main__":
	#argv[1] number of seed to generate
	config = config() 
	flist = os.listdir(config['img_dir'])
	noFile = len(flist)
	ouf = open(config['seed_file'], 'w')
	noSeed = int(argv[1])
	i = 0
	rand = MyRandint()
	seedID = []
	while i < noSeed:
		imgNo = rand(0, noFile)
		imgID = flist[imgNo][:-4]
		if imgID in seedID:
			continue
		fname = config['img_dir']+'/'+imgID+'.jpg'
		img = cv2.imread(fname)
		h, w, d = img.shape
		out_line = random_patch(config['json_dir'], imgID, [1, w], [1, h], [4, 15], w, h)
		if out_line == False:
			continue
		i += 1
		ouf.write(out_line+'\n')
		print i, 'seeds generated'
		seedID.append(imgID)