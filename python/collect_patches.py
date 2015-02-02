import os
from sys import argv
import json
from poseletFunc import *

if __name__ == "__main__":
	#argv[1] lambda
	conf = config()
	lbd = float(argv[1])
	inf = open(conf['seed_file'], 'r') #seed list
	seedlist = inf.readlines()
	inf.close()
	candlist = os.listdir(conf['candidate_dir'])
	tot = len(seedlist)
	tot1 = len(candlist)
	cnt = 0
	for seedline in seedlist:
		imgID1, posInfo, count, kps1 = get_patch_info_from_line(seedline)
		ofile = conf['collected_list_dir']+'/'+imgID1
		for i in range(4):
			ofile += '_'+str(posInfo[i])
		cnt1 = 0
		collected_list = []
		for candId in candlist:
			if candId == '.DS_Store':
				continue
			inf = open(conf['candidate_dir']+'/'+candId, 'r')
			lines = inf.readlines()
			inf.close()
			mind = [100, 100, 100]
			minline = ''
			for line in lines:
				imgID2, posInfo, count, kps2 = get_patch_info_from_line(line)
				try:
					dp, dv = calculate_dis(kps1, kps2)
					d = dp+lbd*dv
					if dp != 100 and dv > 0.06:
						if d < mind[2]:
							mind = [dp, dv, d]
							minline = line
				except:
					pass
			if minline != '':
				collected_list.append((mind, minline))
			cnt1 += 1
			print 'Processing seed', cnt+1, '/', tot, ' , comparing ', cnt1, '/', tot1
		collected_list.sort(key=lambda x:x[0][2])
		ouf = open(ofile, 'w')
		for item in collected_list:
			ouf.write(item[1][:-1]+str(item[0])+'\n')
		ouf.close()
		cnt += 1
		print 'Comparasion of seed', cnt, '/', tot, 'finished'