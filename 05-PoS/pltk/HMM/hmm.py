import pandas as pd
import numpy as np
from tqdm import tqdm
from ..Tokenizer import Normalize

class HMM:
    def __init__(self):
        self.STARTSTATE='$'
        self.stateTransision=pd.DataFrame({'$':[0.0]},index=['$'])
        #   $ S1 S2 S3
        # $ 0
        # S1
        # S2
        # S3
        # indexs are perviuos state
        self.tokenProbability=pd.DataFrame({'':[0.0]},index=['$'])
        #   '' T0 T1 T2
        # $  1 0  0  0
        # S1 0
        # S2 0
        # S3 0
        # indexs are states
    def train(self,doc,verbos=True):
        if type(doc)==str:
            trainData=self.preprocess(doc)
        elif type(doc)==list:
            trainData=doc
        else:
            raise ValueError("doc must be str or list")
        if verbos:
            print(f"the train process started for {len(trainData)} size document")
        previuosState=self.STARTSTATE
        if verbos:
            for tok,state in tqdm(trainData):
                if state not in self.stateTransision:
                    self.stateTransision.loc[state,state]=0
                    self.stateTransision.fillna(0,inplace=True)
                    self.tokenProbability.loc[state,'']=0
                    self.tokenProbability.fillna(0,inplace=True)
                if tok not in self.tokenProbability:
                    self.tokenProbability.loc['$',tok]=0
                    self.tokenProbability.fillna(0,inplace=True)
                self.stateTransision.loc[previuosState,state]+=1
                self.tokenProbability.loc[state,tok]+=1
                previuosState=state
        else:
            for tok,state in trainData:
                if state not in self.stateTransision:
                    self.stateTransision.loc[state,state]=0
                    self.stateTransision.fillna(0,inplace=True)
                    self.tokenProbability.loc[state,'']=0
                    self.tokenProbability.fillna(0,inplace=True)
                if tok not in self.tokenProbability:
                    self.tokenProbability.loc['$',tok]=0
                    self.tokenProbability.fillna(0,inplace=True)
                self.stateTransision.loc[previuosState,state]+=1
                self.tokenProbability.loc[state,tok]+=1
                previuosState=state

        stateRepitition=np.log(self.tokenProbability.sum(axis=1)\
                                                    .to_numpy()\
                                                    .reshape((-1,1)))
        self.stateTransision =np.log(self.stateTransision )-stateRepitition
        self.tokenProbability=np.log(self.tokenProbability)-stateRepitition

        # self.stateTransision.replace([np.inf, -np.inf],0,inplace=True)
        # self.tokenProbability.replace([np.inf, -np.inf],0,inplace=True)

    def preprocess(self,doc):
        doc=open(doc,encoding='utf8')
        docProcessed=[]
        errCount=0
        for index,line in enumerate(doc):
            lineSplit=line[:-1].split(" ")
            if len(lineSplit)==1:
                docProcessed.append(('',self.STARTSTATE))
                continue
            if len(lineSplit)>2 or lineSplit[1]==self.STARTSTATE:
                # print(f"# WARNING: line {index} scaped, {line} because of bad structure...")
                errCount+=1
                continue
            lineSplit[0]=Normalize(lineSplit[0])
            docProcessed.append(tuple(lineSplit))
        doc.close()
        if errCount:
            print(f"# WARNING: {errCount} lines scaped")
        return docProcessed

    def findBestStates(self,tokens):
        # tokens=['']+tokens
        allStates=self.tokenProbability.index
        tokens=[Normalize(tok) for tok in tokens]
        # assert (allStates==self.stateTransision.columns).all()
        predictions=pd.DataFrame(np.zeros((len(self.stateTransision),len(tokens))),
                                 columns=tokens,
                                 index=allStates)-np.inf
        #     t0   t1   t2
        # $  -inf -inf -inf
        # S1 -inf -inf -inf
        # S2 -inf -inf -inf
        # S3 -inf -inf -inf
        for tokIndex,tok in enumerate(tokens):
            for state in allStates:
                try:
                    predictions[tok]=np.maximum(predictions.iloc[:,tokIndex],
                                                self.stateTransision.loc[state].to_numpy()+\
                                                self.tokenProbability.get(tok).to_numpy())
                except AttributeError:
                    predictions[tok]=np.maximum(predictions.iloc[:,tokIndex],
                                                self.stateTransision.loc[state].to_numpy())
                except:
                    print(self.stateTransision.loc[state].to_numpy()+\
                    self.tokenProbability.get(tok).to_numpy())

                    print(predictions[tok])
                    input()
        return list(zip(tokens,
                        [allStates[np.argmax(predictions.iloc[:,tokIndex])] \
                        for tokIndex in range(len(tokens))]))

    def saveModel(self,
                  stateTransisionFilename='stateTransision.csv',
                  tokenProbabilityFilename='tokenProbability.csv'):
        self.stateTransision.to_csv(stateTransisionFilename)
        self.tokenProbability.to_csv(tokenProbabilityFilename)

    def loadModel(self,
                  stateTransisionFilename='stateTransision.csv',
                  tokenProbabilityFilename='tokenProbability.csv'):
        self.stateTransision=pd.read_csv(stateTransisionFilename,index_col=0)
        self.tokenProbability=pd.read_csv(tokenProbabilityFilename,index_col=0)
        tokenProbabilityColumns=list(self.tokenProbability.columns)
        tokenProbabilityColumns[0]=''
        self.tokenProbability.columns=tokenProbabilityColumns

    def test(self,testData):
        numberOfCorrectPredictions=0
        numberOfAllCases=0
        for sent in tqdm(testData):
            taggedSentence=self.findBestStates([i[0] for i in sent])
            numberOfCorrectPredictions+=sum(1 for i,j in\
                                                  zip(taggedSentence,sent)\
                                            if i[1]==j[1])
            numberOfAllCases+=len(taggedSentence)
        return numberOfCorrectPredictions*100/numberOfAllCases
