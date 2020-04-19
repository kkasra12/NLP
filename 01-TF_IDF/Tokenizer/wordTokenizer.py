from re import fullmatch,sub
# import tokens
from .tokens import tokensMap,Token,persionSounds
from time import time

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

def wordTokenizer(text,tokensMap=tokensMap):
    '''
    this function will returns all tokens in the text.
    Parameters:
        text: str
        the string to tokenize
    Returns:
        foundedTokens: list of Toke class
        errorChars:    list of Toke class
    '''
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
                                           sub(persionSounds,"",tmp),
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

if __name__ == '__main__':
    text=open("sampleText").read()
    tokensFile=open("foundedTokens","w")
    errorsFile=open("errorChars","w")
    wordCounterFile=open("wordCounterFile.md","w")
    print("Searching for tokens...")
    startTime=time()
    foundedTokens,errorChars=wordTokenizer(text)
    print(f"Totally {len(foundedTokens)} tokens found in {time()-startTime:.4f}seconds\nwriting the results to files...")
    errorsFile.write("\n".join(str(i)+"\n\tcode: "+str(ord(i.text)) for i in set(errorChars)))
    for i in foundedTokens:
        tokensFile.write(str(i)+"\n")
    wordFrequency=wordCounter(foundedTokens)
    # print(wordFrequency)
    wordCounterFile.write("|index|token|frequency|\n|:-:|:-|:-:|\n")
    wordCounterFile.write("\n".join(f"|{index}|\\{i}|{j}|" for index,(i,j) in enumerate(sorted(wordFrequency.items(),key=lambda x:x[1]))))
