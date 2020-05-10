from pltk import WordProcesses as wp
from time import time

print(f"{len(wp.Dictionary)} tokens loaded...")
myWord=input("Please write your word: ")
nearTerms=wp.suggestWord(myWord)
if nearTerms[0]==[]:
    print(f"your words seems to be wrong, did u mean:"," or ".join(nearTerms[1]))

print("\n\n\ncalculating the time for other algorithms:")
for func in [wp.levenshtein,
             wp.levenshtein_distanceLimiter,
             wp.levenshtein_recursion,
             wp.levenshtein_calculatingNecessaryCells,
             wp.levenshtein_GreedyBFS]:
    startTime=time()
    t1=wp.suggestWord(myWord,editDistanceFunction=func)
    print(f"{func.__name__} calcilation time : {time()-startTime:.2f}s")
    print(f"words with one distance: {t1[1]} and number of words whith 2 distance: {len(t1[2])}\n")
