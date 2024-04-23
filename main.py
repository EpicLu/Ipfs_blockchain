import os
import sys
from ipfs import IpfsClient
from chainblock import BlockChain
from user import User
from datetime import datetime


def main(argv, user, ipfs, block):
    if argv[0] == "-login":
        user.login(argv[1])
    elif argv[0] == "-add":
        timestamp = int(datetime.utcnow().timestamp())
        res = ipfs.upload(argv[1])
        block.addBlock(res, user.curUser, timestamp)
        user.saveItem(res, timestamp)
    elif argv[0] == "-buy":
        if user.curUser is None:
            print("You must login first to use this command!")
            print("-login [username]    Using this command to login.")
            return False
        if block.purchaseItem(argv[1], user.curUser) and \
                user.transferItem(block.getBlock(argv[1]).getIpfsAddr(), user.curUser):
            block.commitPurchase()
            print("Purchase successfully!")
        else:
            print("Error happening! Purchase failed!")

    elif argv[0] == "exit":
        print("goodbye~")
        exit(0)
    else:
        print(
            "Wrong command! Please use the following command.\n" +
            "-login [username]\n" +
            "-add [filepath]\n" +
            "-buy [hash]"
        )


def homepage(user, ipfs, block):
    argv = None
    if len(sys.argv) < 2:
        print("login as a guest...")
    else:
        argv = [sys.argv[1], sys.argv[2]]
        main(argv, user, ipfs, block)

    while True:
        block.show()
        print("--------------------------------------------------------")
        print("-add [filepath]" + "    Using this command to upload a file.")
        print("-buy [hash]" + "    Using this command to buy a item.")
        args = input()
        main(args.split(), user, ipfs, block)

        print("press enter to continue...")
        input()
        os.system("clear")


if __name__ == '__main__':
    bc = BlockChain()
    bcUser = User()
    bcIpfs = IpfsClient()

    historyItems = bcUser.getAllItems()
    for item in historyItems:
        ipfsObj = [{'Hash': item[0], 'Name': item[1], 'Size': str(item[2])}]
        bc.addBlock(ipfsObj, item[4], item[3])

    homepage(bcUser, bcIpfs, bc)
