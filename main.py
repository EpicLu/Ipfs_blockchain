from ipfs import IpfsClient
from chainblock import BlockChain


def main():
    ipfs = IpfsClient()
    res1 = ipfs.upload('test.txt')
    res2 = ipfs.upload('pic.jpg')
    res3 = ipfs.upload('see you again.mp3')

    bc = BlockChain()
    bc.addBlock(res1)
    bc.addBlock(res2)
    bc.addBlock(res3)
    bc.show()


if __name__ == '__main__':
    main()
