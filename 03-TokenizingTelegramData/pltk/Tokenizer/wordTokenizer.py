from .tokens import tokensMap,Token,persianSounds

from re import fullmatch,sub
from tqdm import tqdm

from os.path import dirname,join
DIRNAME=dirname(__file__)

NormalizerFile=open(join(DIRNAME,"normalizerData"))
NormalizerMap={}
for line in NormalizerFile:
    key,value=line.split("->")
    value=value.replace("\n","")
    for char in key:
        assert char not in NormalizerMap, "duplicated character found!!!"
        NormalizerMap.update({char:value})

Normalize=lambda text,NormalizerMap=NormalizerMap:sub(persianSounds,"","".join(NormalizerMap.get(i,i) for i in text))

def textSpliter(t):
    '''
    an internal function which gives text until the nearest space character.
    its used to reduce the execution time.
    '''
    spaceIndex=t.find(" ")+1
    if spaceIndex:
        return (t[:spaceIndex],t[spaceIndex:])
    else:
        return (t,"")

def wordTokenizer(text,tokensMap=tokensMap,Normalizer=Normalize,verbose=0):
    textlst=text.split("\n")
    allTokens=[]
    allErrorChars=[]
    if verbose:
        print()
        for subText in tqdm(textlst,desc="wordTokenizer"):
            tmp=wordTokenizer_(subText,tokensMap=tokensMap,Normalizer=Normalize,verbose=0)
            allTokens+=tmp[0]
            allErrorChars+=tmp[1]
            assert len(tmp)==2
        return allTokens,allErrorChars
    else:
        for subText in textlst:
            tmp=wordTokenizer_(subText,tokensMap=tokensMap,Normalizer=Normalize,verbose=0)
            allTokens+=tmp[0]
            allErrorChars+=tmp[1]
            assert len(tmp)==2
        return allTokens,allErrorChars

def wordTokenizer_(text,tokensMap=tokensMap,Normalizer=Normalize,verbose=0):
    '''
    this function will returns all tokens in the text.
    Parameters:
        text: str
        the string to tokenize
    Returns:
        foundedTokens: list of Toke class
        errorChars:    list of Toke class
    '''
    text=Normalizer(text)
    if verbose:
        print('normalization finished!')
    foundedTokens=[]
    errorChars=[]
    pos=0
    tmp,remainText=textSpliter(text)
    if verbose:
        prePos=0
        progressBar=tqdm(total=len(text))
    while tmp:
        if verbose:
            progressBar.update(n=pos-prePos)
            prePos=pos
        # print(f"'{tmp}'",pos)
        # input()
        # if 'twitter' in tmp:
        #     print(tmp)
        for tokName,tokRegex in tokensMap.items():
            if tokRegex.fullmatch(tmp):
                foundedTokens.append(Token(tokName,
                                           tmp,
                                           tokRegex,
                                           pos=(pos,pos+(len(tmp)))))
                pos+=len(tmp)
                tmp,remainText=textSpliter(remainText)
                break
        else:
            if len(tmp)!=1:
                try:
                    remainText=tmp[-1]+remainText
                except:
                    print("ERR",tmp)
                tmp=tmp[:-1]
            else:
                errorChars.append(Token("ERROR",
                                        tmp,
                                        "NO-REGEX-MATCHES",
                                        pos=(pos,pos+(len(tmp)))))
                pos+=len(tmp)
                tmp,remainText=textSpliter(remainText)
                # continue
    if verbose:
        progressBar.close()
    return foundedTokens,errorChars

def wordCounter(tokensList,verbose=0):
    '''
    returns Term Frequency of tokens
    Returns:
        allwords: dict object
                { <Token class>: <frequency int> }
    '''
    allwords={}
    if verbose:
        print()
        for word in tqdm(tokensList,desc="wordCounter"):
            allwords[word]=allwords.get(word,0)+1
    else:
        for word in tokensList:
            allwords[word]=allwords.get(word,0)+1

    return allwords
