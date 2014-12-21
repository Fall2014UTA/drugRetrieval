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
        self.primitive = ""
        self.concept = ""
        self.kind = ""
        self.value = ""
        self.dict = {}
        self.definingConcepts = []
        self.definingRoles = {}
        self.role = {}
        self.roleg = {}
        self.qualifiers = []
        self.qualifier = {}
        self.roleGroup = []
        self.properties = []
        self.property = {}
        self.associations = []
        self.association = {}
        self.roles = []
        self.roleGroups = []
        self.roleBool = False
        self.qualBool = False
        self.propBool = False
        self.assoBool = False
      
    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "roleGroup":
            self.roleBool = True
        elif tag == "qualifier":
            self.qualBool = True
        elif tag == "property":
            self.propBool = True
        elif tag == "association":
            self.assoBool = True

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "name":
            if (self.name != '' and self.qualBool == False):
                self.dict['name'] = str(self.name)
            elif (self.name != '' and self.qualBool == True):
                self.qualifier['name'] = str(self.name)
            elif (self.name != '' and self.propBool == True):
                self.property['name'] = str(self.name)
            elif (self.name != '' and self.assoBool == True):
                self.association['name'] = str(self.name)
        if self.CurrentData == "value":
            if (self.value != '' and self.qualBool == True):
                self.qualifier['value'] = str(self.value)
            elif (self.value != '' and self.propBool == True):
                self.property['value'] = str(self.value)
            elif (self.value != '' and self.assoBool == True):
                self.association['value'] = str(self.value)
        elif self.CurrentData == "code":
            if self.code != '':
                self.dict['code'] = str(self.code)
        elif self.CurrentData == "id":
            if self.id != '':
                self.dict['id'] = str(self.id)
        elif self.CurrentData == "namespace":
            if self.namespace != '':
                self.dict['namespace'] = str(self.namespace)
        elif self.CurrentData == "primitive":
            if self.primitive != '':
                self.dict['primitive'] = str(self.primitive)
        elif self.CurrentData == "kind":
            if self.kind != '':
                self.dict['kind'] = str(self.kind)
        elif self.CurrentData == "concept":
            self.definingConcepts.append(str(self.concept))
        self.CurrentData = ""
        if tag == 'definingConcepts':
            self.dict['definingConcepts'] = str(self.definingConcepts)
            self.definingConcepts = []
        elif tag == 'conceptDef':
            conceptDef.append(self.dict.copy())
            self.dict.clear()
            self.qualifier.clear()
        elif tag == 'qualifier':
            self.qualifiers.append(self.qualifier.copy())
            self.qualifier.clear()
        elif tag == 'role':
            if self.roleBool == False:
                self.role['name'] = str(self.name)
                self.role['value'] = str(self.value)
                self.role['qualifiers'] = str(self.qualifiers)
                self.qualifiers = []
                self.roles.append(self.role)
                self.role.clear()
            elif self.roleBool == True:
                self.roleg['name'] = str(self.name)
                self.roleg['value'] = str(self.value)
                self.roleg['qualifiers'] = str(self.qualifiers)
                self.qualifiers = []
                self.roleGroup.append(self.roleg)
                self.roleg.clear()
                
        elif tag == 'roleGroup':
            self.roleGroups.append(self.roleGroup)
            self.roleGroup = []
        elif tag == 'definingRoles':
            self.definingRoles['roles'] = self.roles
            self.definingRoles['roleGroups'] = self.roleGroups
            self.dict['definingRoles'] = str(self.definingRoles)
            self.roles = []
            self.roleGroups = []
            self.definingRoles.clear()
#         elif tag = 'property':
#             self.property['qualifiers'] = str(self.qualifiers)

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
        elif self.CurrentData == "primitive":
            self.primitive = content
        elif self.CurrentData == "concept":
            self.concept = content
        elif self.CurrentData == "kind":
            self.kind = content
        elif self.CurrentData == "value":
            self.vlaue = content

conceptDef = []  
      
# create an XMLReader
parser = xml.sax.make_parser()
# turn off namespaces
# parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = ConceptDefHandler()
parser.setContentHandler(Handler)
   
parser.parse("conceptDef.xml")

db = client.rdb
coll=db.ndrf
ndrf_id=coll.insert(conceptDef)
