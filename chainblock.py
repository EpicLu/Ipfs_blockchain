import hashlib
from datetime import datetime


class Block:
    def __init__(self, data, prev_hash):
        self.prev_hash = prev_hash
        self._data = data
        self.timestamp = int(datetime.utcnow().timestamp())

        message = hashlib.sha256()
        message.update(str(self._data[0]['Hash']).encode('utf-8'))
        self.hash = message.hexdigest()

    def getFileName(self):
        return self._data[0]['Name']

    def getIpfsAddr(self):
        return self._data[0]['Hash']

    def getFileSize(self):
        return self._data[0]['Size']


class BlockChain:
    def __init__(self):
        self._blocks = {}

    def addBlock(self, data):
        block = Block(data, self._getPervBlockHash())
        self._blocks[block.hash] = block

    def show(self):
        for key,value in self._blocks.items():
            print('<[hash: ' + key + '], ' 
                  '[file: ' + value.getFileName() + '], '
                  '[size: ' + value.getFileSize() + ' bytes]>')

    def _getPervBlockHash(self):
        res = None
        for key in self._blocks:
            res = self._blocks[key].hash

        return res
