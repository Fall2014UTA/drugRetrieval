
filename = {1 : 'RxTerms201408.txt',
         2 : 'RxTermsArchive201408.txt',
         3 : 'RxTermsIngredients201408.txt'
    }

for key in filename:
    print key,
    print filename[key]
n = raw_input("Select the file number to be parsed: " )

file = ""

def RxTerms201408():
    global file
    file = "RxTerms201408.txt"

def RxTermsArchive201408():
    global file
    file = "RxTermsArchive201408.txt"

def RxTermsIngredients201408():
    global file
    file = "RxTermsIngredients201408.txt"

files = {1 : RxTerms201408,
         2 : RxTermsArchive201408,
         3 : RxTermsIngredients201408
    }

files[int(n)]()

with open(file,'r') as f:
    for line in f:
        print line.replace('|',' ')
    f.close
