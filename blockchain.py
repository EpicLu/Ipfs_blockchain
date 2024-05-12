import hashlib


class Block:
    def __init__(self, data, owner, prev_hash, timestamp):
        self.prev_hash = prev_hash
        self._data = data
        self._timestamp = timestamp
        self._owner = owner

        message = hashlib.sha256()
        message.update(str(self._data['Hash']).encode('utf-8'))
        self.hash = message.hexdigest()

    def setFileOwner(self, buyer):
        self._owner = buyer

    def getFileName(self):
        return self._data['Name']

    def setNewIpfsAddr(self, newCId):
        self._data['Hash'] = newCId

    def getIpfsAddr(self):
        return self._data['Hash']

    def getFileSize(self):
        return self._data['Size']

    def getTimestamp(self):
        return self._timestamp

    def getFileOwner(self):
        return self._owner


class BlockChain:
    def __init__(self):
        self._blocks = {}
        self._boughtItemHashCookies = None
        self._buyer = None
        self._buyerNewCid = None

    def addBlock(self, data, owner: str, timestamp):
        block = Block(data, owner, self._getPervBlockHash(), timestamp)
        self._blocks[block.hash] = block

    def show(self, queryList=None):
        if queryList:
            print("query results:")
            print("|hash\t|" + "file\t|" + "size\t|" + "owner\t")
            for query in queryList:
                print('|' + query.hash +
                      '\t|' + query.getFileName() +
                      '\t|' + query.getFileSize() + ' bytes' +
                      '\t|' + query.getFileOwner()
                      )
            return

        if len(self._blocks) == 0:
            print(r"__        _______ _     ____ ___  __  __ _____       _______")
            print(r"\ \      / / ____| |   / ___/ _ \|  \/  | ____|     /       \ ")
            print(r" \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|      |  O   O  |")
            print(r"  \ V  V / | |___| |__| |__| |_| | |  | | |___     |  ^    ^ |")
            print(r"   \_/\_/  |_____|_____\____\___/|_|  |_|_____|    |_________|")

        else:
            print("|hash\t|" + "file\t|" + "size\t|" + "owner\t")
            for key, value in self._blocks.items():
                print('|' + key +
                      '\t|' + value.getFileName() +
                      '\t|' + value.getFileSize() + ' bytes' +
                      '\t|' + value.getFileOwner()
                      )

    def query(self, queryType, queryValue):
        res = []
        for key, value in self._blocks.items():
            if queryType == '-a' and value.getFileOwner() == queryValue:
                res.append(value)
            elif queryType == '-h' and key == queryValue:
                res.append(value)
            elif queryType == '-f' and value.getFileName()  == queryValue:
                res.append(value)
        if len(res) > 0:
            self.show(res)
        else:
            print("")

    def purchaseItem(self, itemHash, buyer, newCid):
        if itemHash not in self._blocks:
            return False

        owner = self._blocks[itemHash].getFileOwner()
        if buyer == owner:
            print("Cannot purchase your own items!")
            return False
        else:
            print("Enter Y/N to confirm/cancel purchase!")
            decision = input()
            if decision == 'y' or decision == 'Y':
                self._boughtItemHashCookies = itemHash
                self._buyer = buyer
                self._buyerNewCid = newCid
                return True

            return False

    def commitPurchase(self):
        self._blocks[self._boughtItemHashCookies].setFileOwner(self._buyer)
        self._blocks[self._boughtItemHashCookies].setNewIpfsAddr(self._buyerNewCid)

    def getBlock(self, itemHash):
        if itemHash not in self._blocks:
            print("Invalid hash!")
            return None

        return self._blocks[itemHash]

    def getBlocks(self):
        return self._blocks

    def _getPervBlockHash(self):
        res = None
        for key in self._blocks:
            res = self._blocks[key].hash

        return res
