import os
from poseletFunc import *
if __name__ == "__main__":
	conf = config()
	inf1 = open('../00000000011100.kmeans', 'r')
	inf2 = open('../seed_set_sample/00000000011100.sample', 'r')
	lines1 = inf1.readlines()
	lines2 = inf2.readlines()
	inf1.close()
	inf2.close()
	centers = {}
	for i in range(len(lines1)):
		if not lines1[i] in centers.keys():
			centers[lines1[i]] = []
		centers[lines1[i]].append(lines2[i])
	for key in centers.keys():
		odir = '../'+key
		os.mkdir(odir)
		for line in centers[key]:
			extract_patch(line, odir, conf)