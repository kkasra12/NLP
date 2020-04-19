from os import listdir
allFiles=open("AllSamples",'w')
for file in listdir("."):
    if file[:6]=="sample":
        with open(file) as tmp:
            allFiles.write(tmp.read()+"\n---\n")
