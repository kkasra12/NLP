from pltk import Tokenizer as tok
import pandas as pd

# tokens=tok.wordTokenizer(open("TelegramDataset_smaller.txt").read(),verbose=1)[0]
# print(tokens)
t=tok.wordTokenizer(open("TelegramDataset_bigger.txt").read(),verbose=1)
errorCharsFile=open("errorChars",'w')
errorCharsFile.write("\n".join(f"{i.text} {ord(i.text)} {i.pos} {j}" for i,j in tok.wordCounter(t[1]).items()))
errorCharsFile.close()
tokens=t[0]
tokensCount=pd.DataFrame(tok.wordCounter(tokens,verbose=1),index=['termFrequency']).transpose()
tokensCount['text']=[i.text for i in tokensCount.index]
tokensCount['charCode']=[",".join(str(ord(c)) for c in i.text) for i in tokensCount.index]
tokensCount['type']=[i.type for i in tokensCount.index]
tokensCount=tokensCount[['type','text','charCode','termFrequency']].sort_values('text')

print("tokenizerFinished...")
tokensCount.to_excel("tokensCount.xlsx")
print(tokensCount)
