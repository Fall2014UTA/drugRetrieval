
filename = {1 : 'DEMO13Q4.txt',
         2 : 'DRUG13Q4.txt',
         3 : 'INDI13Q4.txt',
         4 : 'OUTC13Q4.txt',
         5 : 'REAC13Q4.txt',
         6 : 'RPSR13Q4.txt',
         7 : 'THER13Q4.txt'
    }
for key in filename:
    print key,
    print filename[key]
n = raw_input("Select the file number to be parsed: " )

file = ""

def DEMO13Q4():
    global file
    file = "DEMO13Q4.txt"

def DRUG13Q4():
    global file
    file = "DRUG13Q4.txt"

def INDI13Q4():
    global file
    file = "INDI13Q4.txt"

def OUTC13Q4():
    global file
    file = "OUTC13Q4.txt"

def REAC13Q4():
    global file
    file = "REAC13Q4.txt"

def RPSR13Q4():
    global file
    file = "RPSR13Q4.txt"

def THER13Q4():
    global file
    file = "THER13Q4.txt"

files = {1 : DEMO13Q4,
         2 : DRUG13Q4,
         3 : INDI13Q4,
         4 : OUTC13Q4,
         5 : REAC13Q4,
         6 : RPSR13Q4,
         7 : THER13Q4
    }

files[int(n)]()

with open(file,'r') as f:
    for line in f:
        print line.replace('$',' ')
    f.close
