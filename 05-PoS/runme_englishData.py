from nltk.corpus import treebank
from nltk.tag import hmm
from pltk.HMM import HMM

def DataAdapter(nltkData):
    AdaptedData=[]
    for sent in nltkData:
        AdaptedData+=[('','$')]
        AdaptedData+=sent
    return AdaptedData
TRAIN_DATA_SIZE=0.8
try:
    all_data = treebank.tagged_sents()
except LookupError:
    print("Downloading treebank")
    import nltk
    nltk.download('treebank')
    all_data = treebank.tagged_sents()
train_data=all_data[:int(len(all_data)*TRAIN_DATA_SIZE)]
test_data=all_data[int(len(all_data)*TRAIN_DATA_SIZE):]

# print("using nltk.tag.hmm.HiddenMarkovModelTrainer\n")
# trainer = hmm.HiddenMarkovModelTrainer()
# tagger = trainer.train_supervised(train_data)
#
# print(tagger.tag("Today is a good day .".split()))
# print(tagger.tag("Joe met Joanne in Delhi .".split()))
# print(tagger.tag("Chicago is the birthplace of Ginny".split()))
#
# tagger.test(test_data)

print("using pltk.HMM.HMM (implemented by myself)")
myHmm=HMM()
# myHmm.train(DataAdapter(train_data))
# myHmm.saveModel()

myHmm.loadModel()
# print(myHmm.findBestStates("Today is a good day .".split()))
# print(myHmm.findBestStates("Joe met Joanne in Delhi .".split()))
# print(myHmm.findBestStates("Chicago is the birthplace of Ginny".split()))

print(myHmm.test(test_data))
