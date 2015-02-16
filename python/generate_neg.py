import os
from sys import argv
import cv2
from poseletFunc import *
if __name__ == "__main__":
	conf = config()
	flist = os.listdir(conf['neg_seed_img_dir'])
	ouf = open(conf['neg_seed_file'], 'w')
	cnt = 0
	tot = len(flist)
	for f in flist:
		imgID = f[:-4]
		fname = conf['neg_seed_img_dir']+'/'+f
		img = cv2.imread(fname)
		h, w, d = img.shape
		i = 0
		while i < 10:
			out_line = random_patch(imgID, [1, w], [1, h], [6, 7], w, h)
			if out_line != False:
				ouf.write(out_line+'\n')
				i += 1
		cnt += 1
		print cnt, '/', tot, 'finished'
	ouf.close()