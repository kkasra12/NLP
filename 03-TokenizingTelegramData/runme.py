from pltk import Tokenizer as tok
import pandas as pd

# tokens=tok.wordTokenizer(open("TelegramDataset_smaller.txt").read(),verbose=1)[0]
# print(tokens)
tokens=tok.wordTokenizer(open("TelegramDataset_bigger.txt").read(),verbose=1)[0]
tokensCount=pd.DataFrame(tok.wordCounter(tokens,verbose=1),index=['termFrequency']).transpose()
tokensCount['text']=[i.text for i in tokensCount.index]
tokensCount['type']=[i.type for i in tokensCount.index]
tokensCount=tokensCount[['type','text','termFrequency']].sort_values('text')

print("tokenizerFinished...")
tokensCount.to_excel("tokensCount.xlsx")
print(tokensCount)
