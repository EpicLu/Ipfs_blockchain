from datetime import datetime
import datasketch
import pickle
import jieba
import os


def tokenize(text):
    return jieba.lcut(text)


def readMinHashObj():
    res = []
    for file_name in os.listdir("./lshData"):
        file_path = os.path.join("./lshData", file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                res.append(pickle.load(f))
    return res


def genMinHashObj(text):
    tokens = tokenize(text)
    minhash = datasketch.MinHash(num_perm=128)

    for token in tokens:
        minhash.update(token.encode('utf-8'))

    return minhash


class MinhashObj:
    def __init__(self, minhashObj, filename):
        self.minhashObj = minhashObj
        self.filename = filename


class LSHVerify:
    def __init__(self, oldTexts, filenames):
        self._minhashObjSet = []
        self._initMinHashObj(oldTexts, filenames)

    def _initMinHashObj(self, oldTexts, filenames):
        folderPath = os.path.join(os.getcwd(), "lshData")
        if os.path.exists(folderPath):
            for fn in os.listdir(folderPath):
                fp = os.path.join(folderPath, fn)
                if os.path.isfile(fp):
                    os.remove(fp)

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        for i in range(len(oldTexts)):
            self._saveMinHashObj(genMinHashObj(oldTexts[i]), filenames[i])

    def _saveMinHashObj(self, minhashObj, filename):
        saveObj = MinhashObj(minhashObj, filename)
        with open(f"./lshData/{filename.replace('.', '_')}_{int(datetime.utcnow().timestamp())}", 'wb') as f:
            pickle.dump(saveObj, f)
        self._minhashObjSet.append(saveObj)

    def verify(self, text, filename):
        newMinHash = genMinHashObj(text)

        for i in range(len(self._minhashObjSet)):
            obj = self._minhashObjSet[i]
            similarity = newMinHash.jaccard(obj.minhashObj)
            # print(str(similarity))
            if similarity > 0.5:
                print(f"This work has a similarity of {similarity * 100}% with \"{obj.filename}\"!")
                return False

        self._saveMinHashObj(newMinHash, filename)
        return True


# ot = []
# fns = ["test.txt", "不一样的爱.txt"]
# for fn in fns:
#     with open(f"{fn}", 'r') as f:
#         ot.append(f.read())

# lsh = LSHVerify(ot, fns)

# with open("缓慢而优雅的成长.txt", "r") as f:
#     ret = lsh.verify(f.read(), "缓慢而优雅的成长.txt")
#     print(ret)
