import sys
from ipfs import IpfsClient
from chainblock import BlockChain
from user import User


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


def entry(argv):
    if argv < 2:
        print("login as a guest...")
        return

    if argv[1] == "login":
        User.login(argv[1])


def homepage():
    # ming tian zai zuo
    main()


if __name__ == '__main__':
    main()
