from scipy.cluster.hierarchy import fclusterdata
import numpy as np
from sklearn.cluster import KMeans
def assignpeople(ngos,people):
	data=ngos+people
	state=None
	datanp=np.zeros((len(data),2))
	for k,i in enumerate(data):
		datanp[k,0]=i[1]
		datanp[k,1]=i[2]

	cluster=fclusterdata(datanp,1)
	print(cluster)
	cnt=0
	for k in range(len(ngos)):
		ngos[k].append(cluster[cnt])
		ngos[k].append(1)
		cnt+=1
	for k in range(len(people)):
		people[k].append(cluster[cnt])
		people[k].append(0)
		cnt+=1
	data=people+ngos
	data.sort(key = lambda x: x[3])
	i=0
	curr=data[0][3]
	while i<len(data):
		currdata=[]
		j=i
		while data[i][3]==curr:
			currdata.append(data[i])
			i+=1
		curr=data[i][3]
		isone=False
		cntngo=0
		cntppl=0
		iszero=False
		for c in currdata:
			if c[4]==1:
				isone=True
				cntngo+=1
			elif c[4]==0:
				iszero=True
				cntppl+=1
		if isone and iszero:
			d=np.zeros((len(currdata),2))
			for u,f in enumerate(currdata):
				d[u,0]=f[1]
				d[u,1]=f[2]
			clustersmall=KMeans(n_clusters=cntngo, random_state=0).fit(d)
			lblcnt=0
			tmplblcnt=0
			taken={}
			for t in range(cntppl):
				currdata[t].append(clustersmall.labels_[lblcnt])
				lblcnt+=1
			prev=-1
			tmplblcnt=lblcnt
			for t in range(cntngo):
				if clustersmall.labels_[lblcnt] not in taken:
					currdata[lblcnt].append(clustersmall.labels_[lblcnt])
					taken[clustersmall.labels_[lblcnt]]=1
				lblcnt+=1
			for t in range(tmplblcnt, tmplblcnt+cntngo):
				if len(currdata[t])==5:
					for ss in range(cntngo):
						if ss not in taken:
							taken[ss]=1
							currdata[t].append(ss)
							break
			for x,c in enumerate(currdata):
				if c[4]==0:
					for x1,c1 in enumerate(currdata):
						if x1==x:
							continue
						elif c1[4]==1 and c1[5]==c[5]:
							currdata[x].append(c1[0])
							break
				elif c[4]==1:
					reslat=0
					leslat=0
					for x1,c1 in enumerate(currdata):
						elif c1[4]==0 and c1[5]==c[5]:
							reslat+=c1[1]/3
							reslon+=c1[2]/3
					currdata[x].append(reslat)
					currdata[x].append(reslon)			

			restorecnt=0
			while j<i:
				data[j]=currdata[restorecnt]
				j+=1
				restorecnt+=1
		elif iszero and not isone:
			temp=i
			obtained=False
			while temp<	
		print(data)

if __name__=='__main__':
	assignpeople()
