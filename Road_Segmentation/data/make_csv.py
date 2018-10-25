import csv
import os
csv = open('tile_log.csv','w')
columnTitleRow = "img, downloaded\n"
csv.write(columnTitleRow)
dic={}
for i in os.listdir('/media/rick/7B3A33754CA4427C/codefundo_code/label/'):
	dic[str(i)]=1
for key in dic.keys():
	name = key
	email = dic[key]
	row = name + "," + str(email) + "\n"
	csv.write(row)

