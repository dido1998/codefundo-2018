import cv2
import os
import numpy as np
for i in os.listdir('label/'):
	print(i)
	if i==".fuse_hidden0003f7eb00000001":
		continue
	img = cv2.imread('label/'+i,0)
	ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	if(np.mean(th2)==255):
		os.system("rm label/"+i)
		os.system("rm train/"+i)
	elif(np.mean(th2)<=4.5):
		os.system("rm label/"+i)
		os.system("rm train/"+i)

