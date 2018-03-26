import pickle

localDict = {}

with open('CET_4.txt', 'r') as f1:
    lst1 = f1.readlines()
    for i in lst1:
        word = i.split()[0]
        trans = i.split()[1]
        localDict[word] = trans
with open('CET_6.txt', 'r') as f2:
    lst2 = f2.readlines()
    for i in lst2:
        word = i.split()[0]
        trans = i.split()[1]
        localDict[word] = trans

dictfile = open('localDict.pkl', 'wb')
pickle.dump(localDict, dictfile)
dictfile.close()
