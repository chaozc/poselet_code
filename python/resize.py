import cv2
import os
import numpy as np
from sys import argv
if __name__ == "__main__":
	flist = os.listdir(argv[1])
	cnt = 1
	tot = len(flist)-1
	for f in flist:
		if not '.jpg' in f:
			continue
		fname = argv[1]+'/'+f
		print 'Resizing ', fname, cnt, '/', tot
		image = cv2.imread(fname)
		try:
			w, h, d = image.shape
			if w > h:
				size = (int(round(h*600/w)), 600)
			else:
				size = (600, int(round(w*600/h)))
			rsz = cv2.resize(image, size)
			cv2.imwrite(argv[2]+'/'+f, rsz)
		except:
			print 'Some Error Occured'
		cnt += 1
