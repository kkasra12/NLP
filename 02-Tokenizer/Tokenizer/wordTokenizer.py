from re import fullmatch,sub
# import tokens
from .tokens import tokensMap,Token,persianSounds
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

def wordTokenizer(text,tokensMap=tokensMap,Normalizer=Normalize):
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
    foundedTokens=[]
    errorChars=[]
    pos=0
    tmp,remainText=textSpliter(text)
    while tmp:
        # print(f"'{tmp}'",pos)
        # input()
        for tokName,tokRegex in tokensMap.items():
            if fullmatch(tokRegex,tmp):
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
    return foundedTokens,errorChars

def wordCounter(tokensList):
    '''
    returns Term Frequency of tokens
    Returns:
        allwords: dict object
                { <Token class>: <frequency int> }
    '''
    allwords={}
    for word in tokensList:
        allwords[word]=allwords.get(word,0)+1
    return allwords
