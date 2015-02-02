from sys import argv
import subprocess
import os
if __name__ == "__main__":
	flist = os.listdir(argv[1])
	i = 0
	tot = len(flist)
	for f in flist:
		if '.json' in f:
			try:
				subprocess.call(['cp', argv[2]+'/'+f[:len(f)-5]+'.jpg', argv[3]])
				i += 1
				print f[:len(f)-5]+'.jpg', 'copied', i, '/', tot
			except:
				print 'Some error occured'
