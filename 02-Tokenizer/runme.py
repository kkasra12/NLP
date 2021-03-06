import Tokenizer as tok
import documentStaticals as ds
from time import time
def makeDfReadyToSave(df):
    newDf=df.copy()
    newDf["TokenText"]=[t.text for t in df.index]
    newDf["TokenType"]=[t.type for t in df.index]
    newDf=newDf[["TokenType","TokenText"]+list(df.columns)]
    return newDf
if __name__ == '__main__':
    # corpusName="CorpusSmall"
    corpusName="CorpusBig"
    # corpusName="TelegramCorpus"
    startTime=time()
    tf=ds.TF(corpusName,outputFormat="pandas_DataFrame")
    print(f"The TF matrix is calculated in {time()-startTime}\n{tf}\n{'-'*50}")
    startTime=time()
    df=ds.DF_fromTF(tf)
    print(f"The DF matrix is calculated in {time()-startTime}\n{df}\n{'-'*50}")
    # startTime=time()
    # df=DF(corpusName,outputFormat="pandas_DataFrame")
    # print(f"The DF matrix is calculated in {time()-startTime}\n{df}\n{'-'*50}")
    startTime=time()
    tf_idf=ds.TF_IDF(tf,df,outputFormat="pandas_DataFrame")
    print(f"The TF-IDF matrix is calculated in {time()-startTime}\n{tf_idf}\n{'-'*50}")

    print("saving files...")
    makeDfReadyToSave(tf).to_excel("tf.xlsx")
    print("\tTF saved...")
    makeDfReadyToSave(df).to_excel("df.xlsx")
    print("\tDF saved...")
    makeDfReadyToSave(tf_idf).to_excel("tf_idf.xlsx")
    print("\tTF-IDF saved...")
