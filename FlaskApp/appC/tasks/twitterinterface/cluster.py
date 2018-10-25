from scipy.cluster.hierarchy import fclusterdata
import numpy as np
from sklearn.cluster import KMeans
from appC.tasks.twitterinterface import database as db
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

"""
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
			db.insertngocurr(ngo[min][0],str(p[1]),str(p[2]),p[0])
			db.insertrescuengo(p[0],ngo[min][0])

"""
def precluster(people,ngo):
	print("in precluster!!!!")
	for p in people:
		p.append(1)
	for n in ngo:
		n.append(0)
	data=people
	newngo=[]
	datanp=np.zeros((len(data),2))
	for i,d in enumerate(data):
		if len(d)==5:
			datanp[i,0]=d[1]
			datanp[i,1]=d[2]
	if len(data)>1:	
		cluster=fclusterdata(datanp,1)
	else:
		cluster=[0]	
	for i,d in enumerate(data):
		d.append(cluster[i])
	data.sort(key=lambda x:x[5])
		
	curr=data[0][5]
	i=0
	while i<len(data):
		temp=[]
		while i<len(data) and data[i][5]==curr:
			temp.append(data[i])
			i+=1
		if i<len(data):
			curr=data[i][5]
		cenlat=0
		cenlon=0
		for t in temp:
			cenlat+=t[1]/len(temp)
			cenlon+=t[2]/len(temp)
		minindex=0
		min=ngo[0]
		for n in ngo:
			if haversine(n[5],n[4],cenlon,cenlat)< haversine(min[5],min[4],cenlon,cenlat):
				min=n
		for t in temp:
			print("inserting!!!!!!")
			db.insertngocurr(min[0],str(t[1]),str(t[2]),t[0])
			db.commit()
			db.insertrescuengo(t[0],min[0])
			db.commit()
			
	

