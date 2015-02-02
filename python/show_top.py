import os
from sys import argv
import subprocess
from poseletFunc import *
if __name__ == "__main__":
	#argv[2]: top number
	conf = config()
	flist = os.listdir(conf['collected_list_dir'])
	cnt = 0
	tot = len(flist)
	for f in flist:
		if f != '.DS_Store':
			odir = conf['sample_dir']+'/'+f
			os.mkdir(odir)
			subprocess.call(['cp', conf['seed_patches_dir']+'/'+f+'.jpg', odir])
			os.mkdir(odir+'/samples')
			subprocess.call(['python', 'extract_patch.py', conf['collected_list_dir']+'/'+f, odir+'/samples', argv[1]])
			cnt += 1
			print cnt, '/', tot, 'finished'

