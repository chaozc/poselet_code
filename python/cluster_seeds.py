from poseletFunc import *
import os
if __name__ == "__main__":
	conf = config()
	inf = open(conf['seed_file'], 'r')
	lines = inf.readlines()
	inf.close()
	clusters = {}
	for line in lines:
		imgID, posInfo, cnt, kps = get_patch_info_from_line(line)
		kpConfID = kp_config_id(kps)
		if not kpConfID in clusters.keys():
			clusters[kpConfID] = [line]
		else:
			clusters[kpConfID].append(line)
	for kpConfID in clusters.keys():
		ofile = conf['seed_set_file_dir']+'/'+kpConfID
		ouf = open(ofile, 'w')
		for line in clusters[kpConfID]:
			ouf.write(line)
		ouf.close()
		odir = conf['seed_set_patches_dir']+'/'+kpConfID
		os.mkdir(odir)
		extract_patches(conf, ofile, odir)