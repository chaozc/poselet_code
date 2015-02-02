import os
from sys import argv
import subprocess
if __name__ == "__main__":
	#argv[1]: collision file
	#argv[2]: origin img dir
	#argv[3]: duplicated img dir
	inf = open(argv[1], 'r')
	lines = inf.readlines()
	cnt = 0
	tot = len(lines)
	for line in lines:
		param = line.split(' ')
		param = param[2:]
		for it in param[:-1]:
			fname = argv[2]+'/'+it+'.jpg'
			try:
				subprocess.call(['mv', fname, argv[3]])
			except:
				print 'some error occured'
		cnt += 1
		print 'finished', cnt, '/', tot