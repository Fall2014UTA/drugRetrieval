
import pymongo
from pymongo import MongoClient
import csv

client = MongoClient('50.84.62.186', 27017)
client.rdb.authenticate('rdb', 's6LGndHa')
my_list=[]
keys=[]
arr=[0,2,4,5,7,8,9,10,11]


dict2={}
key=''
name=''

def build_ing():
	print
	with open('RxTermsIng.txt','rb') as ing:
		reader = csv.reader(ing, delimiter='|', quotechar='\n') 
		next(reader)
		for row in reader:
			dict3={}
			key=str(row[0])
			name=str(row[1])
			dict3['INGREDIENT']=name
			dict3['ING_RXCUI']=str(row[2])
			
			if key in dict2:
				dict2[key].append(dict3)
			else:
				dict2[key]=[dict3]


def load_file(name):
	print
	with open(name, 'rb') as csvfile:
			table = csv.reader(csvfile, delimiter='|', quotechar='\n')  
			keys=csvfile.readline()
			keys=keys.split('|')
			#print keys
		
			for row in table:
				my_dict={}
				for i in arr:
					if(row[i]!=''):
						my_dict[keys[i]]=row[i]
				if row[0] in dict2:
					my_dict['INGREDIENTS']=dict2[row[0]]
					 
				my_list.append(my_dict)
build_ing()
load_file('RxTerms1.txt')
load_file('RxTerms2.txt')	


db = client.rdb
coll=db.rxterms
rxterms_id=coll.insert(my_list)


