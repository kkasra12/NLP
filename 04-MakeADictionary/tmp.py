# from pltk import Tokenizer as tok
#
# t=tok.wordCounter(tok.wordTokenizer(open("Allwords1").read(),verbose=1)[0])
# open("Allwords2",'w').write("\n".join([i.text for i in t if i.type in ['PERSIAN_WORD']]))

f0=set(open("AllWords").read().split("\n"))
f1=open("AllWords1").read().split("\n")
assert len(f0)==len(set(f0)),print(len(f0)-len(set(f0)))
assert len(f1)==len(set(f1))
print(len(f0),len(f1))
f1=set(f1)
f1.update(f0)
open("WordsDataset",'w').write("\n".join(f1))
