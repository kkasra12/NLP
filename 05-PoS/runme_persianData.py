from nltk.tag import hmm
from pltk.HMM import HMM
from pltk.Tokenizer import Normalize

def DataAdapter(nltkData):
    AdaptedData=[]
    for sent in nltkData:
        AdaptedData+=[('','$')]
        AdaptedData+=sent
    return AdaptedData
TRAIN_DATA_SIZE=0.8

doc=open("PoS.txt",encoding='utf8')
STARTSTATE='$'
all_data=[]
errCount=0
currentSent=[]
for index,line in enumerate(doc):
    lineSplit=line[:-1].split(" ")
    if len(lineSplit)==1:
        all_data.append(currentSent)
        currentSent=[]
        continue
    if len(lineSplit)>2:
        errCount+=1
        continue
    lineSplit[0]=Normalize(lineSplit[0])
    currentSent.append(tuple(lineSplit))
doc.close()
if errCount:
    print(f"# WARNING: {errCount} lines scaped")
train_data=all_data[:int(len(all_data)*TRAIN_DATA_SIZE)]
test_data=all_data[int(len(all_data)*TRAIN_DATA_SIZE):]

TestSentences=[
"اولین سیاره خارج از منظومه شمسی دیده شد .",
"طی سالهای اخیر ممکن است تعدادی سیاره خارج از منظومه شمسی دیده باشند ."
]

print("using nltk.tag.hmm.HiddenMarkovModelTagger\n")
tagger = hmm.HiddenMarkovModelTagger.train(train_data)

print("\n".join(str(tagger.tag(i.split())) for i in TestSentences))

tagger.test(test_data)

print("using pltk.HMM.HMM (implemented by myself)")
myHmm=HMM()
myHmm.train(DataAdapter(train_data))
myHmm.saveModel()

# myHmm.loadModel()
print("\n".join(str(myHmm.findBestStates(i.split())) for i in TestSentences))

print(myHmm.test(test_data))
