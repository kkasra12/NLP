from pltk.HMM import HMM

myHmm=HMM()
myHmm.train("./PoS.txt")
myHmm.saveModel()

myHmm.loadModel()
print(myHmm.stateTransision)
print(myHmm.tokenProbability)

print(myHmm.findBestStates(["اولين","سياره","خارج","از","منظومه","شمسي","ديده","شد","."]))
print(myHmm.findBestStates(["طی","سالهای","اخیر","ممکن","است","اولین","سیاره","خارج","از","منظومه","شمسی","دیده","باشند",".",]))
