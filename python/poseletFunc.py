import json
from MyRandint import MyRandint
import numpy as np
import cv2
import math

def config():
	inf = open('config.json')
	config = json.load(inf)
	inf.close()
	return config

def KP_in_Patch(stx, sty, xsz, ysz, x, y):
	if (stx <= x) and (x < stx+xsz) and (sty <= y) and (y < sty+ysz):
		return [x-stx, y-sty]
	else:
		return False

def get_KPs_from_JSON(jsondir, imgID, stx, sty, xsz, ysz):
	inf = open(jsondir+'/'+imgID+'.json')
	data = json.load(inf)
	inf.close()
	if len(data['point']) != 14:
		return False
	kps = []
	for xy in data['point']:
		kp = KP_in_Patch(stx, sty, xsz, ysz, xy[0], xy[1])
		kps.append(kp)
	return kps

def in_center(stx, sty, xsz, ysz, left, right, top, bottom):
	if left*6 > xsz and left*5 < 2*xsz and right*6 < 5*xsz and right*5 > 3*xsz:
		if top*6 > ysz and top*5 < 2*ysz and bottom*6 < 5*ysz and bottom*5 > 3*ysz:
			return True
	return False

def patch_info(jsondir, imgID, stx, sty, xsz, ysz):
	kps = get_KPs_from_JSON(jsondir, imgID, stx, sty, xsz, ysz)
	left = 1000; right = 0; top = 1000; bottom = 0; cnt = 0;
	if kps != False:	
		for kp in kps:
			if kp != False:
				cnt += 1
				left = min(left, kp[0])
				right = max(right, kp[0])
				top = min(top, kp[1])
				bottom = max(right, kp[1])
	return kps, cnt, left, right, top, bottom

def random_patch(jsondir, imgID, rand_stx, rand_sty, rand_sz, w, h):
	stx = np.random.randint(rand_stx[0], rand_stx[1])
	sty = np.random.randint(rand_sty[0], rand_sty[1])
	sz = np.random.randint(rand_sz[0], rand_sz[1])
	xsz = sz*16
	ysz = sz*24
	if (stx+xsz < w) and (sty+ysz < h):
		kps, cnt, left, right, top, bottom = patch_info(jsondir, imgID, stx, sty, xsz, ysz)
		if kps == False:
			return False
		if cnt > 0 and in_center(stx, sty, xsz, ysz, left, right, top, bottom):
			return imgID+'#'+str([stx, sty, xsz, ysz])+'#'+str(cnt)+'#'+'_'.join([str(it) for it in kps])+'#'
	return False

def get_patch_info_from_line(line):
	param = line.split('#')
	imgID = param[0]
	p1 = param[1][1:-1].split(', ')
	posInfo = [int(it) for it in p1]
	cnt = int(param[2])
	p3 = param[3].split('_')
	kps = []
	for item in p3:
		if item == 'False':
			kps.append(False)
		else:
			kp = item[1:-1].split(', ')
			kps.append([float(it) for it in kp])
	return imgID, posInfo, cnt, kps
	"""
	if param[4] == '\n':
		return imgID, posInfo, cnt, kps
	else:
		p4 = param[4][1:-1.split(', ')]
		d = p4[float(it) for it in p4]
		return imgID, posInfo, cnt, kps, d
	"""

def extract_patch(line, odir, conf):
	imgID, posInfo, cnt, kps = get_patch_info_from_line(line)
	img = cv2.imread(conf['img_dir']+'/'+imgID+'.jpg')
	patch = img[posInfo[1]:posInfo[1]+posInfo[3], posInfo[0]:posInfo[0]+posInfo[2]]
	if conf['draw_kp_in_patches'] == 'True':
		for kp in kps:
			if kp != False:
				point = (int(kp[0]), int(kp[1]))
				cv2.circle(patch, point, 3, (0, 0, 255), -1)
				cv2.circle(patch, point, 4, (0, 255, 255), 1)
	fname = odir+'/'+imgID
	for i in range(4):
		fname += '_'+str(posInfo[i])
	fname += '.jpg'
	cv2.imwrite(fname, patch)

def calculate_dis(kps1, kps2):
	ckps1 = []
	ckps2 = []
	union = 0
	intersection = 0
	for i in range(14):
		if kps1[i] != False and kps2[i] != False:
			ckps1.append(kps1[i])
			ckps2.append(kps2[i])
			intersection += 1
		if kps1[i] != False or kps2[i] != False:
			union += 1
	Dp = Procrustes_distance()(ckps1, ckps2, intersection)
	Dv = float(intersection)/union
	return Dp, Dv
	
class Procrustes_distance:
	def __init__(self):
		self.yes = True
	
	#Calculate mean & scale
	def mean_scale(self, pch, kpNum):
		xmean = sum([kp[0] for kp in pch])
		ymean = sum([kp[1] for kp in pch])
		xmean /= kpNum
		ymean /= kpNum

		scale = sum([(kp[0]-xmean)**2+(kp[1]-ymean)**2 for kp in pch])
		scale /= kpNum
		scale = math.sqrt(scale)

		if scale < 1:
			scale = 1
		return xmean, ymean, scale

	#Remove the Translation & Uniform Scaling Components
	def tans_uniScale(self, pch, xmean, ymean, scale):
		return [[(kp[0]-xmean)/scale, (kp[1]-ymean)/scale] for kp in pch]

	#Remove the Rotation Components, then calculate the Procrustes distance
	def rot_dis(self, pch1, pch2, kpNum):
		sum1 = sum([pch2[i][0]*pch1[i][1]-pch2[i][1]*pch1[i][0] for i in range(kpNum)])
		sum2 = sum([pch2[i][0]*pch1[i][1]+pch2[i][1]*pch1[i][0] for i in range(kpNum)])
		if sum2 != 0:
			theta = math.atan(sum1/sum2)
		else:
			theta = math.asin(1)
		sin = math.sin(theta)
		cos = math.cos(theta)
		rotpch = [[cos*kp[0]-sin*kp[1], sin*kp[0]+cos*kp[1]] for kp in pch2]
		return math.sqrt(sum([(pch1[i][0]-rotpch[i][0])**2+(pch1[i][1]-rotpch[i][1])**2 for i in range(kpNum)]))
	def __call__(self, pch1, pch2, kpNum):
		if kpNum == 0:
			return 100
		xmean, ymean, scale = self.mean_scale(pch1, kpNum)
		pch1 = self.tans_uniScale(pch1, xmean, ymean, scale)
		xmean, ymean, scale = self.mean_scale(pch2, kpNum)
		pch2 = self.tans_uniScale(pch2, xmean, ymean, scale)
		return self.rot_dis(pch1, pch2, kpNum)