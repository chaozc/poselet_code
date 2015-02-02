import math
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