import Tokenizer as tok
from os import path,listdir
import pandas as pd
from time import time
def TF(documents,outputFormat='sparseMatrix'):
    '''
    Parameters:
        documents: string, list
            an string contains a folder name of corpus or list of documents
        outputFormat: string
            'sparseMatrix' or 'pandas_DataFrame'
    returns:
        <class dict>
        { <class str> documentName: <class dict>
                                    { <class Token> : <class int> frequency }}
    '''
    if type(documents)==str:
        if not path.isdir(documents):
            raise ValueError("you must give me a folder name or list of files")
        documents=[path.join(documents,i) for i in listdir(documents) if path.isfile(path.join(documents,i))]
        if len(documents)==0:
            raise ValueError("this folder is empty or has no file!!!")
    if type(documents)==list:
        if not all(path.isfile(i) for i in documents):
            raise ValueError("no file is this directory!!!")
    else:
        raise ValueError("you must give me a folder name or list of files")

    if outputFormat not in ['sparseMatrix', 'pandas_DataFrame']:
        raise ValueError("The outputFormat must be 'sparseMatrix' or 'pandas_DataFrame'")


    TF_mat={}
    for fileName in documents:
        if not fileName in TF_mat:
            fileObj=open(fileName)
            TF_mat.update({fileName:tok.wordCounter(tok.wordTokenizer(fileObj.read())[0])})
            fileObj.close()
    if outputFormat=='sparseMatrix':
        return TF_mat
    elif outputFormat=="pandas_DataFrame":
        return pd.DataFrame(TF_mat,columns=sorted(documents)).fillna(0).sort_index()


def DF(documents,outputFormat='sparseMatrix'):
    '''
    Parameters:
        documents: string, list
            an string contains a folder name of corpus or list of documents
        outputFormat: string
            'sparseMatrix' or 'pandas_DataFrame'
    Returns: <class dict>
        { <class Token> : <class int> DocumentFrequency}
    '''
    if type(documents)==str:
        if not path.isdir(documents):
            raise ValueError("you must give me a folder name or list of files")
        documents=[path.join(documents,i) for i in listdir(documents) if path.isfile(path.join(documents,i))]
        if len(documents)==0:
            raise ValueError("this folder is empty or has no file!!!")
    if type(documents)==list:
        if not all(path.isfile(i) for i in documents):
            raise ValueError("no file is this directory!!!")
    else:
        raise ValueError("you must give me a folder name or list of files")

    if outputFormat not in ['sparseMatrix', 'pandas_DataFrame']:
        raise ValueError("The outputFormat must be 'sparseMatrix' or 'pandas_DataFrame'")


    documents=set(documents)
    DF_mat={}
    for fileName in documents:
        fileObj=open(fileName)
        for token in set(tok.wordTokenizer(fileObj.read())[0]):
            DF_mat[token]=DF_mat.get(token,0)+1
    if outputFormat=="sparseMatrix":
        return DF_mat
    elif outputFormat=="pandas_DataFrame":
        return pd.DataFrame.from_dict(DF_mat,orient = 'index',columns=['DocumentFrequency']).sort_index()


def TF_IDF(TF_mat,DF_mat,outputFormat='sparseMatrix'):
    '''
        Parameters:
            TF_mat:
                the output of TF function
            DF_mat:
                the output of DF or DF_fromTF function
            outputFormat: string
                'sparseMatrix' or 'pandas_DataFrame'
        Returns: <class dict>
        { <class str> documentName: <class dict>
                                    { <class Token> : <class float> TF-IDF value }}
    '''
    if type(TF_mat)==dict and type(DF_mat)==dict:
        TFIDF_mat={doc:{token:TF_mat[doc][token]/DF_mat[token] for token in TF_mat[doc]} for doc in TF_mat}
    elif type(TF_mat)==pd.DataFrame and type(DF_mat)==pd.DataFrame:
        duplicated_df=pd.DataFrame([])
        for col in TF_mat.columns:
            duplicated_df[col]=DF_mat['DocumentFrequency']
        return TF_mat/duplicated_df
    else:
        raise ValueError("both TF and DF must be dict or pandas.DataFrame")

    if outputFormat not in ['sparseMatrix', 'pandas_DataFrame']:
        raise ValueError("The outputFormat must be 'sparseMatrix' or 'pandas_DataFrame'")

    if outputFormat=="sparseMatrix":
        return TFIDF_mat
    elif outputFormat=="pandas_DataFrame":
        return pd.DataFrame(TFIDF_mat).fillna(0).sort_index()

def DF_fromTF(TF_mat):
    if type(TF_mat)==dict:
        DF_mat={}
        for doc in TF_mat:
            for token in TF_mat[doc]:
                DF_mat[token]=DF_mat.get(token,0)+1
        return DF_mat
    elif type(TF_mat)==pd.DataFrame:
        DF_mat=TF_mat/TF_mat
        return pd.DataFrame(DF_mat.count(axis='columns'),columns=["DocumentFrequency"])


if __name__ == '__main__':
    # corpusName="CorpusSmall"
    corpusName="CorpusBig"
    startTime=time()
    tf=TF(corpusName,outputFormat="pandas_DataFrame")
    print(f"The TF matrix is calculated in {time()-startTime}\n{tf}\n{'-'*50}")
    startTime=time()
    df=DF_fromTF(tf)
    print(f"The DF matrix is calculated in {time()-startTime}\n{df}\n{'-'*50}")
    # startTime=time()
    # df=DF(corpusName,outputFormat="pandas_DataFrame")
    # print(f"The DF matrix is calculated in {time()-startTime}\n{df}\n{'-'*50}")
    startTime=time()
    tf_idf=TF_IDF(tf,df,outputFormat="pandas_DataFrame")
    print(f"The TF-IDF matrix is calculated in {time()-startTime}\n{tf_idf}\n{'-'*50}")

    print("saving files...")
    tf.to_excel("tf.xlsx")
    df.to_excel("df.xlsx")
    tf_idf.to_excel("tf_idf.xlsx")
