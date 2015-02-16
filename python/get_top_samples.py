from poseletFunc import *
import os
from sys import argv
if __name__ == "__main__":
	#argv[1]: top n
	n = int(argv[1])
	conf = config()
	flist = os.listdir(conf['seed_set_file_dir'])
	tot = len(flist)
	cnt = 0
	for f in flist:
		if f != '.DS_Store':
			inf = open(conf['seed_set_file_dir']+'/'+f, 'r')
			lines = inf.readlines()
			ouf = open(conf['seed_set_sample_dir']+'/'+f+'.sample', 'w')
			toplines = []
			for line in lines:
				imgID, posInfo, cntt, kps = get_patch_info_from_line(line)
				fname = conf['collected_list_dir']+'/'+imgID
				for i in range(4):
					fname += '_'+str(posInfo[i])
				tpls = top_lines(fname, n)
				for tpl in tpls:
					pos = tpl.rfind('#')
					if not tpl[:pos] in toplines:
						toplines.append(tpl[:pos])
			for tpl in toplines:
				ouf.write(tpl+'\n')
			ouf.close()
			cnt += 1
			print 'Set', cnt, '/', tot, 'finished'