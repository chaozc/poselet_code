from poseletFunc import *
import matplotlib.pyplot as plt
if __name__ == "__main__":
	conf = config()
	inf = open(conf['seed_file'])
	lines = inf.readlines()
	inf.close()
	cnts = []
	rc = [0]*15
	kpconf = {'top':[13], 'mid':[6, 7, 8, 9, 10, 11], 'bottom':[0, 1, 4, 5], 'top-mid-connect-point':[12], 'mid-bottom-connect-point':[2, 3]}
	confkeys = ['top', 'mid', 'bottom', 'top-mid-connect-point', 'mid-bottom-connect-point']
	kpsconf = [0, 0, 0, 0, 0]
	value = {'top':1, 'mid':10, 'bottom':100, 'top-mid-connect-point':1000, 'mid-bottom-connect-point':10000}
	cate = {'1':'top', '10':'mid', '11':'top-mid', '100':'bottom', '101':'top-bottom', '110':'mid-bottom', '111':'top-mid-bottom', '1000':'top-mid-connect-point', '10000':'mid-bottom-connect-point'}
	kpcnts = {'top':0, 'mid':0, 'top-mid':0, 'bottom':0, 'top-bottom':0, 'mid-bottom':0, 'top-mid-bottom':0, 'mid-bottom-connect-point':0, 'top-mid-connect-point':0}
	for line in lines:
		imgID, posInfo, cnt, kps = get_patch_info_from_line(line)
		cnts.append(cnt)
		rc[cnt] += 1
		kpconfig = {}
		for key in confkeys:
			kpconfig[key] = False
		for i in range(14):
			if kps[i] != False:
				for key in confkeys:
					if i in kpconf[key]:
						kpconfig[key] = True
		v = 0
		for key in confkeys:
			if kpconfig[key]:
				v += value[key]
		if v%1000 > 0:
			v = v%1000
		kpcnts[cate[str(v)]] += 1

	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax4 = plt.subplot(212)
	n, bins, patches = ax1.hist(cnts, 15)
	ax1.set_xlabel('Number of key points')
	ax1.set_ylabel('Number of seeds')
	ax1.axis([0, max(cnts), 0, min([i*50 for i in range(11) if i*50 > max(n)])])
	ax1.grid(True)
	piequant = [it for it in rc if it > 0]
	label = [str(i)+' kps' for i in range(15) if rc[i] > 0]
	ax2.pie(piequant, labels=label)

	piequant = [kpcnts[key] for key in kpcnts.keys() if kpcnts[key] > 0]
	label = [key for key in kpcnts.keys() if kpcnts[key] > 0]
	ax4.pie(piequant, labels=label)
	plt.show()