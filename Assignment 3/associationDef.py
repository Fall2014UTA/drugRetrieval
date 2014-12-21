import xml.sax
from pymongo import MongoClient

client = MongoClient('50.84.62.186', 27017)
client.rdb.authenticate('rdb', 's6LGndHa')

class ConceptDefHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.name = ""
        self.code = ""
        self.id = ""
        self.namespace = ""
        self.inverseName = ""
        self.dict = {}
      
    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "name":
            if self.name != '':
                self.dict['name'] = str(self.name)
        elif self.CurrentData == "code":
            if self.code != '':
                self.dict['code'] = str(self.code)
        elif self.CurrentData == "id":
            if self.id != '':
                self.dict['id'] = str(self.id)
        elif self.CurrentData == "namespace":
            if self.namespace != '':
                self.dict['namespace'] = str(self.namespace)
        elif self.CurrentData == "inverseName":
            if self.inverseName != '':
                self.dict['inverseName'] = str(self.inverseName)
        self.CurrentData = ""
        if tag == 'associationDef':
            associationDef.append(self.dict.copy())
            self.dict.clear()

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "code":
            self.code = content
        elif self.CurrentData == "id":
            self.id = content
        elif self.CurrentData == "namespace":
            self.namespace = content
        elif self.CurrentData == "inverseName":
            self.inverseName = content
   
associationDef = [] 
       
# create an XMLReader
parser = xml.sax.make_parser()
# turn off namespaces
# parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = ConceptDefHandler()
parser.setContentHandler(Handler)
   
parser.parse("associationDef.xml")

db = client.rdb
coll=db.ndrf
ndrf_id=coll.insert(associationDef)