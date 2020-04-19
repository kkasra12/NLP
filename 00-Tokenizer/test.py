def test(n):
    a=[1,2,4]
    b=[7,7,2]
    return a,b

print(test(4))
for i,j in zip(*test(4)):
    print(i,j)
