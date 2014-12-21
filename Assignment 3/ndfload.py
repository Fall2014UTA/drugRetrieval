
import csv
import pymongo
from pymongo import MongoClient

client = MongoClient('50.84.62.186', 27017)
client.rdb.authenticate('rdb', 's6LGndHa')
my_list=[]

with open('NDFRT_Public_2014.07.07_NUI.txt', 'rb') as csvfile:
	table = csv.reader(csvfile, delimiter='\t', quotechar='\n')  
	for row in table:
		my_list.append({row[-1]:row[0]})
		#s=s+row[-1]+","+row[0]+"\n"
db = client.rdb
coll=db.medicine
med_id=coll.insert(my_list)
