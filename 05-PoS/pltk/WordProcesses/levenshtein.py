import numpy as np
from os import chdir
from os.path import dirname,join
from time import time

DIRNAME=dirname(__file__)
DictionaryFile=open(join(DIRNAME,"WordsDataset"),encoding='utf8')
Dictionary=DictionaryFile.read().split("\n")
DictionaryFile.close()

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    matrix[:,0]=np.arange(size_x)
    matrix[0,:]=np.arange(size_y)
    for x in range(1,size_x):
        for y in range(1,size_y):
            if seq1[x-1] == seq2[y-1]:
                # matrix [x,y] = min(
                #     matrix[x-1, y] + 1,
                #     matrix[x-1, y-1],
                #     matrix[x, y-1] + 1)
                matrix[x,y]=matrix[x-1,y-1]
            else:
                matrix [x,y] = min(
                    matrix[x-1,y],
                    matrix[x-1,y-1],
                    matrix[x,y-1])+1
    return int(matrix[size_x-1,size_y-1])

def levenshtein_distanceLimiter(seq1, seq2,maxDis=2):
    maxDis+=1
    stepOver=lambda point,step:[point[0]+step[0],point[1]+step[1]]
    size_x=len(seq1)+1
    size_y=len(seq2)+1
    matrix=np.zeros((size_x, size_y))+maxDis+1
    matrix[:,0]=np.arange(size_x)
    matrix[0,:]=np.arange(size_y)
    startPoint=[1,1]
    steps=[(0,1),(1,0)]
    k=0
    while startPoint[0]<size_x and startPoint[1]<size_y:
        point=startPoint
        while point[0]<size_x and point[1]<size_y:
            x,y=point
            if seq1[x-1] == seq2[y-1]:
                matrix[x,y]=matrix[x-1,y-1]
            else:
                matrix [x,y] = min(
                    matrix[x-1,y],
                    matrix[x-1,y-1],
                    matrix[x,y-1])+1
            if maxDis<matrix[x,y]:
                break
            point=stepOver(point,steps[k])
        k=(k+1)%2
        startPoint=stepOver(startPoint,steps[k])
    return int(matrix[size_x-1,size_y-1])

def levenshtein_calculatingNecessaryCells(seq1,seq2):
    if seq2=="":
        return len(seq1)
    size_x=len(seq1)+1
    size_y=len(seq2)+1
    matrix=np.zeros((size_x, size_y))-1
    matrix[:,0]=np.arange(size_x)
    matrix[0,:]=np.arange(size_y)
    queue_findOptimalPath=[(size_x-1,size_y-1)]
    visitedCells=set()
    stack_calculatedCells=[]
    while queue_findOptimalPath:
        currentCell=queue_findOptimalPath.pop(0)
        visitedCells.add(currentCell)
        if seq1[currentCell[0]-1]==seq2[currentCell[1]-1]:
            cell=(currentCell[0]-1,currentCell[1]-1)
            if cell not in visitedCells and\
               (cell[0]!=0 and cell[1]!=0) and\
               cell not in queue_findOptimalPath:
                queue_findOptimalPath.append(cell)
            stack_calculatedCells.append((currentCell,cell))
        else:
            for cell in [(currentCell[0]-1,currentCell[1]),
                         (currentCell[0],currentCell[1]-1),
                         (currentCell[0]-1,currentCell[1]-1)]:
                if cell not in visitedCells and\
                   (cell[0]!=0 and cell[1]!=0) and\
                   cell not in queue_findOptimalPath:
                    queue_findOptimalPath.append(cell)

            stack_calculatedCells.append((currentCell,
                                          (currentCell[0]-1,currentCell[1]),
                                          (currentCell[0],currentCell[1]-1),
                                          (currentCell[0]-1,currentCell[1]-1)))
    while stack_calculatedCells:
        currentCell=stack_calculatedCells.pop(-1)
        if len(currentCell)==2:
            matrix[currentCell[0]]=min([matrix[i] for i in currentCell[1:]])
        else:
            matrix[currentCell[0]]=min([matrix[i] for i in currentCell[1:]])+1

    return int(matrix[size_x-1,size_y-1])

def levenshtein_recursion(seq1,seq2):
    if seq2=="":
        return len(seq1)
    size_x=len(seq1)+1
    size_y=len(seq2)+1
    matrix=np.zeros((size_x, size_y))-1
    matrix[:,0]=np.arange(size_x)
    matrix[0,:]=np.arange(size_y)
    return int(recursive_levenshtein(seq1,seq2,matrix,(size_x-1,size_y-1)))
def recursive_levenshtein(seq1,seq2,matrix,cell):
    if matrix[cell]==-1:
        x,y=cell
        if seq1[x-1] == seq2[y-1]:
            matrix[x,y]=recursive_levenshtein(seq1,seq2,matrix,(x-1,y-1))
        else:
            matrix [x,y] = min(
                recursive_levenshtein(seq1,seq2,matrix,(x-1,y)),
                recursive_levenshtein(seq1,seq2,matrix,(x-1,y-1)),
                recursive_levenshtein(seq1,seq2,matrix,(x,y-1)))+1
    return matrix[cell]

def levenshtein_GreedyBFS(seq1,seq2):
    if seq2=="":
        return len(seq1)
    size_x=len(seq1)+1
    size_y=len(seq2)+1
    treeChilds={} # { <childCell> : (<fatherCell>,<cost: 0 or 1>) }
    currentCell=(size_x-1,size_y-1)
    if seq1[currentCell[0]-1]==seq2[currentCell[1]-1]:
        zeroCostQueue=[currentCell]
        oneCostQueue=[]
    else:
        zeroCostQueue=[]
        oneCostQueue=[currentCell]
    while 1:
        if len(zeroCostQueue)!=0:
            zeroCostQueue.sort()
            currentCell=zeroCostQueue.pop(0)
            if currentCell[0]==0:
                valueOfCurrentCell=currentCell[1]
                break
            if currentCell[1]==0:
                valueOfCurrentCell=currentCell[0]
                break
            newCell=(currentCell[0]-1,currentCell[1]-1) # generate childCell
            if newCell in treeChilds: # avoid redundancy
                continue
            treeChilds.update({newCell:(currentCell,0)}) # update tree
            if seq1[newCell[0]-1]==seq2[newCell[1]-1]: # add new cells to queue
                zeroCostQueue.append(newCell)
            else:
                oneCostQueue.append(newCell)
        elif len(oneCostQueue)!=0:
            oneCostQueue.sort()
            currentCell=oneCostQueue.pop(0)
            if currentCell[0]==0:
                valueOfCurrentCell=currentCell[1]
                break
            if currentCell[1]==0:
                valueOfCurrentCell=currentCell[0]
                break
            newCells=[(currentCell[0]-1,currentCell[1]),
                      (currentCell[0],currentCell[1]-1),
                      (currentCell[0]-1,currentCell[1]-1)]
            for newCell in newCells:
                if newCell in treeChilds: # avoid redundancy
                    continue
                treeChilds.update({newCell:(currentCell,1)}) # update tree
                if seq1[newCell[0]-1]==seq2[newCell[1]-1]:
                    zeroCostQueue.append(newCell)
                else:
                    oneCostQueue.append(newCell)
        else:
            raise Exception("unreachable state :(")
    while currentCell!=(size_x-1,size_y-1):
        valueOfCurrentCell+=treeChilds[currentCell][1]
        currentCell=treeChilds[currentCell][0]
    return int(valueOfCurrentCell)


def suggestWord(word,Dictionary=Dictionary,editDistanceFunction=levenshtein,maxDis=2):
    response=[[] for _ in range(maxDis+1)]
    for w in Dictionary:
        editDistance=editDistanceFunction(word,w)
        if editDistance<=maxDis:
            response[editDistance].append(w)
    if editDistanceFunction.__name__=="levenshtein_GreedyBFS":
        return suggestWord(word,Dictionary=response[0]+response[1],maxDis=maxDis)
    return response

if __name__ == '__main__':
    # print(levenshtein_GreedyBFS("کسری","مقتولین"))
    testCases=["kasra","kasia","parvin"]
    print("\t"+"\t".join(testCases))
    for i in testCases:
        print(i,end="\t")
        print("\t".join(f"{levenshtein(i,j)}" for j in testCases))
    algorithms=[levenshtein_GreedyBFS,
                levenshtein,
                levenshtein_distanceLimiter,
                levenshtein_recursion,
                levenshtein_calculatingNecessaryCells,]
    for func in algorithms:
        startTime=time()
        t1=suggestWord("کسری",editDistanceFunction=func)
        print(f"{func.__name__} :{time()-startTime:.2f}")
        print(t1[1],len(t1[2]))
