from datetime import datetime
import datasketch
import pickle
import jieba
import os

chunk_size = 100


def tokenize(text):
    return jieba.lcut(text)


def genMinHashObj(text):
    tokens = tokenize(text)
    minhash = datasketch.MinHash(num_perm=128)

    for token in tokens:
        minhash.update(token.encode('utf-8'))

    return minhash


def saveMinHashObj(minhashObj, filename):
    with open(f"./lshData/{filename.replace('.', '_')}_{int(datetime.utcnow().timestamp())}", 'wb') as f:
        pickle.dump(MinhashObj(minhashObj, filename), f)


def readMinHashObj():
    res = []
    for file_name in os.listdir("./lshData"):
        file_path = os.path.join("./lshData", file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                res.append(pickle.load(f))
    return res


def initMinHashObj(oldTexts, filenames):
    folderPath = os.path.join(os.getcwd(), "lshData")
    if os.path.exists(folderPath):
        for fn in os.listdir(folderPath):
            fp = os.path.join(folderPath, fn)
            if os.path.isfile(fp):
                os.remove(fp)

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    for i in range(len(oldTexts)):
        saveMinHashObj(genMinHashObj(oldTexts[i]), filenames[i])


class LSHVerify:
    def __init__(self, oldTexts, filenames):
        initMinHashObj(oldTexts, filenames)
        self._minhashObjSet = readMinHashObj()

    def verify(self, text, filename):
        newMinHash = genMinHashObj(text)

        for i in range(len(self._minhashObjSet)):
            obj = self._minhashObjSet[i]
            similarity = newMinHash.jaccard(obj.minhashObj)
            # print(str(similarity))
            if similarity > 0.5:
                print(f"This work has a similarity of {similarity * 100}% with \"{obj.filename}\"!")
                return False

        saveMinHashObj(newMinHash, filename)
        self._minhashObjSet.append(newMinHash)
        return True


class MinhashObj:
    def __init__(self, minhashObj, filename):
        self.minhashObj = minhashObj
        self.filename = filename

# ot = []
# fns = ["test.txt", "test1.txt"]
# for fn in fns:
#     with open(f"{fn}", 'r') as f:
#         ot.append(f.read())

# lsh = LSHVerify(ot, fns)

# with open("test2.txt", "r") as f:
#     ret = lsh.verify(f.read(), "test2.txt")
#     print(ret)
