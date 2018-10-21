from scipy.cluster.hierarchy import fclusterdata
import numpy as np
from sklearn.cluster import KMeans
import FlaskApp.app as app
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km


def assignpeople(people,ngos):
	cntngo=len(ngos)
	d=np.zeros((len(people),2))
	for i,p in enumerate(people):
		d[i,0]=p[1]
		d[i,1]=p[2]
	clustersmall=KMeans(n_clusters=cntngo, random_state=0).fit(d)
	for i,p in enumerate(people):
		p.append(clustersmall[i])
	people.sort(lambda x:x[5])
	taken={}
	curr=people[0][5]
	i=0
	while i<len(people):
		temp=[]
		while people[i][5]==curr:
			temp.append(people[i])
			i+=1
		curr=people[i][5]
		curlat=0
		curlng=0
		for t in temp:
			curlat+=t[1]/3
			curlng+=t[2]/3
		min=0
		mindist=1000000
		for j,n in enumerate(ngo):
			if j in taken:
				continue
			else:
				dist=haversine(n[6],n[5],curlng,curlat)
				if dist<mindist:
					mindist=dist
					min=j
		for p in people:
			app.insertngocurr(ngo[min][0],p[1],p[2],p[0])
			app.insertrescuengo(p[0],ngo[min][0])


def precluster(people,ngo):
	for p in people:
		p.append(1)
	for n in ngo:
		n.append(0)
	data=people+ngo
	newngo=[]
	datanp=np.zeros((len(data),2))
	for i,d in enumerate(data):
		if len(d)==5:
			datanp[i,0]=d[1]
			datanp[i,1]=d[2]
		else:
			datanp[i,0]=d[5]
			datanp[i,1]=d[6]
	cluster=fclusterdata(datanp,1)
	initcnt=len(people)
	for w,n in enumerate(ngo):
		cnt=0
		for e,p in enumerate(people):
			if cluster[e]==cluster[initcnt+w]:
				cnt+=1
		if cnt>0:
			newngo.append(n)
	cluster(people,newngo)
if __name__=='__main__':
	assignpeople()
