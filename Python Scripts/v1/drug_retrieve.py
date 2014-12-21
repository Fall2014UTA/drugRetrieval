from pymongo import MongoClient
from bson.json_util import dumps
import ast
import pprint
from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

@app.route('/api/v1/drugs/<string:drug_name>', methods=['GET'])
def getDataMongo(drug_name):
	qry=1					#Flag to check the string in url type (combination or single string) to optimize performance
	if not "_" in drug_name:
		qry=0
	drug_name=drug_name.replace('_',' ')
	drug_name=drug_name.replace('+','/')
	
	client=MongoClient('mongodb://<database name>:s<password>@<i.p. address of db>') #Establish connection with mongodb database
	ndfrt_cursor=client.rdb.ndfrt
	rxterm_cursor=client.rdb.rxterms
	fda_cursor=client.rdb.fdaCollection
	
	#Taking starting point of query from INDEXED name id in ndrft to find all records matching the result
	
	#In case of single medicine name or query used regular expressions to find all related names from database else directly point using the eq operator
	
	if qry==0:
		results=ndfrt_cursor.find({'name':{'$regex':'^'+drug_name+''}})
	else:
		results=ndfrt_cursor.find({'name':{'$eq':drug_name}})
	#Declaring drug list to add all related data together
	drug_list=[]
	drug_dict=dict()
	#Declaring list and dict for all the 3 collections
	ndfrt_list=[]
	ndfrt_dict=dict()
	rxterm_list=[]
	rxterm_dict=dict()
	fda_list=[]
	fda_dict=dict()
	
	full_genric_name=None
	
	ndfrt_genric_name_list=[]
	flag=0
	for record in results:
		ndfrt_list.append(record)
		ndfrt_properties= record['properties'] # Extract properties string from the output to get genric name which is unique in rxterms
		if(flag==5):
			break;
		flag=flag+1
		ndfrt_properties = ndfrt_properties[1:-1]
		ndfrt_properties=ndfrt_properties.replace("{","")
		ndfrt_properties=ndfrt_properties.replace("}","")
		ndfrt_properties=dumps(ndfrt_properties)
		split_array=ndfrt_properties.split(",")
		pos_cursor=0
		getpos_name=0
		for i in split_array:
			if "C819" in i:
				getpos_name=pos_cursor+1
				break;							#Find C819 which is property for full genric name and extract it from string. Then break from loop
			pos_cursor=pos_cursor+1
		full_genric_name=split_array[getpos_name]
		full_genric_name=full_genric_name[11:-2]
		ndfrt_genric_name_list.append(full_genric_name)
	
	ndfrt_dict['ndfrt']=ndfrt_list
	drug_list.append(ndfrt_dict)
		
	ingredient_list=[]
	for h in ndfrt_genric_name_list:
		results=rxterm_cursor.find(({"FULL_GENERIC_NAME" :{"$eq":h}})) #Extract the data from rxterm using full genric name
		for record in results:
			rxterm_list.append(record)
			if(record.has_key('INGREDIENTS')):							#Finding all ingredients in that particular drug or its composition
				ingredient=record['INGREDIENTS']
				ingredient=list(ingredient)
				for i in ingredient:
					a=dumps(i)
					a=a.split(",")
					a=a[1]
					a=a[16:-2]
					ingredient_list.append(a)
	ingredient_list=list(set(ingredient_list)) # Get Unique ingredients from the list
	rxterm_dict['rxterms']=rxterm_list
	drug_list.append(rxterm_dict)
	for i in ingredient_list:										#Get all the FDA data for ingredients present in a drug with demographic, drug, reaction ,outcome
		results=fda_cursor.find({"drugname":{"$eq":i.upper()}})		#information
		for record in results:
			fda_list.append(record)
			
	fda_dict['fda']=fda_list
	drug_list.append(fda_dict)									#add data in dictionary to be displayed 
	return dumps(drug_list).replace("\\",'')					#Formatting the data
	
if __name__ == '__main__':
	app.run(debug=True)
