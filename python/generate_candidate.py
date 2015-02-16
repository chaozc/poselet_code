import cv2
import os
import numpy as np
from sys import argv
from MyRandint import MyRandint
from poseletFunc import *
if __name__ == "__main__":
	#argv[1]: num of bin
	conf = config()
	flist = os.listdir(conf['img_dir'])
	noFile = len(flist)
	cntImg = 0
	totPatch = 0
	rand = MyRandint()
	bsz = int(argv[1])
	for f in flist:
		fname = conf['img_dir']+'/'+f
		if fname.find('.jpg') > 0:
			imgID = f[:-4]
			img = cv2.imread(fname)
			h, w, d = img.shape
			xbin = w/bsz
			ybin = h/bsz
			cntPatch = 0
			ouf = open(conf['candidate_dir']+'/'+f[:-4], 'w')
			for i in range(bsz):
				for j in range(bsz):
					for k in range(500):
						out_line = random_patch(imgID, [i*xbin, (i+1)*xbin], [j*ybin, (j+1)*ybin], [4, 15], w, h, conf['json_dir'])
						if out_line != False:
							cntPatch += 1
							ouf.write(out_line+'\n')
			ouf.close()
			cntImg += 1
			totPatch += cntPatch
			print cntImg, '/', noFile, 'img finished,  Patches for img:', cntPatch, 'Total Patches:', totPatch 