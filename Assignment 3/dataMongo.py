import csv
from pymongo import MongoClient

client = MongoClient(host="50.84.62.186", port=27017)
client.rdb.authenticate('rdb','s6LGndHa')
# get a db
db = client['rdb']  # or client.your_db_name

collection = db['fdaCollection']  # or db.publishers
#d=[]
#key=["primaryid","caseid","indi_drug_seq","indi_pt"]
#publisher ={"primaryid":"","caseid":"","indi_drug_seq":"","indi_pt":""}
keyDrug=["primaryid","drug_seq","role_cod","drugname","nda_num"]
keyDemo=["primaryid","i_f_code","age","age_cod","gndr_code","reporter_country"]
keyIndi=["primaryid","caseid","indi_drug_seq","indi_pt"]
keyOut=["primaryid","caseid","outc_cod"]
keyRpsr=["primaryid","caseid","rpsr_cod"]
keyTher=["primaryid","caseid","dsg_drug_seq"]
keyReac=["primaryid","caseid","pt"]
outDict={}
reacDict={}
rpsrDict={}
therDict={}
drugDict=[]
demoDict={}
indiDict={}

keyPos=[0,3,11,12,13,20]
keyDrugPos=[0,2,3,4,14]
keyIndiPos=[0,1,2,3]# all positions
keyOutPos=[0,1,2]
keyReacPos=[0,1,2]
keyRpsrPos=[0,1,2]
keyTherPos=[0,1,2]


with open('RPSR13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(0,len(keyRpsr)):
			if row[i]!=None:
				d[keyRpsr[i]]=row[keyRpsrPos[i]]
				
		#print "############### " 
		rpsrDict[row[0]]=d
		#print rpsrDict

with open('REAC13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(1,len(keyReac)):
			if row[i]!=None:
				d[keyReac[i]]=row[keyReacPos[i]]
				
		#print "############### " 
		reacDict[row[0]]=d
		#print reacDict

with open('OUTC13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(1,len(keyOut)):
			if row[i]!=None:
				d[keyOut[i]]=row[keyOutPos[i]]
				
		#print "############### " 
		outDict[row[0]]=d
		#print outDict

with open('INDI13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(1,len(keyIndi)):
			if row[i]!=None:
				d[keyIndi[i]]=row[keyIndiPos[i]]
				
		#print "############### " 
		indiDict[row[0]]=d
		#print indiDict


with open('DEMO13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(1,len(keyDemo)):
			if row[i]!=None:
				d[keyDemo[i]]=row[keyPos[i]]
				
		#print " ############### " 
		demoDict[row[0]]=d
		#print demoDict


with open('THER13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(1,len(keyTher)):
			if row[i]!=None:
				d[keyTher[i]]=row[keyTherPos[i]]
				
#		#print "############### " 
		#print d
		therDict[row[0]]=d

		#print therDict

#print "############### $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" 
with open('DRUG13Q4.txt') as f:
	reader = csv.reader(f, delimiter='$', quoting=csv.QUOTE_NONE)
    # skip the headers
	next(reader, None)

	for row in reader:
		d={}
		for i in range(0,len(keyDrug)):
			if row[i]!=None:
				d[keyDrug[i]]=row[keyDrugPos[i]]
				
		##print "############### " 
		#print d
		key=row[0]
		if key in therDict:
			d['therapy']=therDict[key]
		if key in reacDict:
			d['reaction']=reacDict[key]
		if key in outDict:
			d['outcome']=outDict[key]
		if key in rpsrDict:
			d['rspr']=rpsrDict[key]
		if key in indiDict:
			d['demo']=demoDict[key]
		if key in indiDict:
			d['Indication']=indiDict[key]
		#print therDict[key]
		
		drugDict.append(d)
		#print drugDict
		#print drugDict
fdaId=collection.insert(drugDict)		



