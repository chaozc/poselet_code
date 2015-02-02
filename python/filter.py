import os
from sys import argv
if __name__ == "__main__":
	#argv[1] collected patches dir
	#argv[2] lambda
	#argv[3] output dir
	dirlist = os.listdir(argv[1])
	lbd = float(argv[2])
	cnt = 0
	tot = len(dirlist)
	for d in dirlist:
		if d != '.DS_Store':
			cnt += 1
			print 'Processing seed ', cnt, '/', tot
			dd = argv[1]+'/'+d
			flist = os.listdir(dd)
			slist = []
			for f in flist:
				if f != '.DS_Store':
					fname = dd+'/'+f
					inf = open(fname, 'r')
					lines = inf.readlines()
					inf.close()
					mscore = 100
					mline = ''
					for line in lines:
						param = line.split('###')
						scores = param[0].split(' ')
						s = float(scores[0])+lbd*float(scores[1])
						if s < mscore:
							mscore = s
							mline = param[1]
					if mscore < 100:
						slist.append((mscore, mline))
			slist.sort(key=lambda x:x[0])
			ouf = open(argv[3]+'/'+d, 'w')
			for it in slist:
				ouf.write(it[1])
			ouf.close()