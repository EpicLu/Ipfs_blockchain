import hashlib


class Block:
    def __init__(self, data, owner, prev_hash, timestamp):
        self.prev_hash = prev_hash
        self._data = data
        self._timestamp = timestamp
        self._owner = owner

        message = hashlib.sha256()
        message.update(str(self._data[0]['Hash']).encode('utf-8'))
        self.hash = message.hexdigest()

    def setFileOwner(self, buyer):
        self._owner = buyer

    def getFileName(self):
        return self._data[0]['Name']

    def getIpfsAddr(self):
        return self._data[0]['Hash']

    def getFileSize(self):
        return self._data[0]['Size']

    def getTimestamp(self):
        return self._timestamp

    def getFileOwner(self):
        return self._owner


class BlockChain:
    def __init__(self):
        self._blocks = {}
        self._boughtItemHash = None
        self._buyer = None

    def addBlock(self, data, owner: str, timestamp):
        block = Block(data, owner, self._getPervBlockHash(), timestamp)
        self._blocks[block.hash] = block

    def show(self):
        if len(self._blocks) == 0:
            print("""
                _______ 
               /       \\
              |  O   O  |
              |  ^    ^ |
              |_________|
            """)
        else:
            print("|hash\t|" + "file\t|" + "size\t|" + "owner\t")
            for key, value in self._blocks.items():
                print('|' + key +
                      '\t|' + value.getFileName() +
                      '\t|' + value.getFileSize() + ' bytes' +
                      '\t|' + value.getFileOwner()
                      )

    def purchaseItem(self, itemHash, buyer):
        owner = self._blocks[itemHash].getFileOwner()
        if buyer == owner:
            print("Cannot purchase your own items!")
            return False
        else:
            print("Enter Y/N to confirm/cancel purchase!")
            decision = input()
            if decision == 'y' or decision == 'Y':
                self._boughtItemHash = itemHash
                self._buyer = buyer
                return True

            return False

    def commitPurchase(self):
        self._blocks[self._boughtItemHash].setFileOwner(self._buyer)

    def getBlock(self, itemHash):
        return self._blocks[itemHash]

    def _getPervBlockHash(self):
        res = None
        for key in self._blocks:
            res = self._blocks[key].hash

        return res
