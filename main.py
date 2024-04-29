import os
import sys
from ipfs import IpfsClient
from blockchain import BlockChain
from user import User
from datetime import datetime
from lsh import LSHVerify


def main(argv, user, ipfs, bc, lshv):
    if argv[0] == "-login":
        user.login(argv[1])
    elif argv[0] == "-add":
        if not isLogin(user):
            return

        if os.path.isdir(argv[1]):
            print("Folder is not supported")
            return
        elif os.path.isfile(argv[1]):
            with open(argv[1], 'r') as f:
                if lshv.verify(f.read(), os.path.basename(argv[1])):
                    timestamp = int(datetime.utcnow().timestamp())
                    res = ipfs.upload(argv[1])
                    bc.addBlock(res, user.curUser, timestamp)
                    user.saveItem(res, timestamp)
                else:
                    print("Upload failed! Suspected plagiarism in the work.")
        else:
            print("Invalid path!")
            return
    elif argv[0] == "-buy":
        if not isLogin(user):
            return

        block = bc.getBlock(argv[1])
        if bc.purchaseItem(argv[1], user.curUser) \
                and block is not None \
                and user.transferItem(block.getIpfsAddr(), user.curUser):
            bc.commitPurchase()
            print("Purchase successfully!")
        else:
            print("Error happening! Purchase failed!")
    elif argv[0] == "-download":
        block = bc.getBlock(argv[1])
        if block is None:
            return
        if permitDownload(user, block):
            cid = block.getIpfsAddr()
            if len(argv) > 2:
                ipfs.download(cid, block.getFileName(), argv[2])
            else:
                ipfs.download(cid, block.getFileName())
        else:
            print("Download failed! Not the owner.")
    else:
        print(
            "Wrong command! Please use the following command.\n" +
            "-login [username]\n" +
            "-add [filepath]\n" +
            "-buy [hash]\n" +
            "-download [hash] [path]"
        )


def homepage(user, ipfs, bc):
    lshv = initLSHVerify(bc.getBlocks(), ipfs)
    if len(sys.argv) < 2:
        print("login as a guest...")
    else:
        argv = [sys.argv[1], sys.argv[2]]
        main(argv, user, ipfs, bc, lshv)

    while True:
        bc.show()
        print("--------------------------------------------------------")
        print("-add [filepath]" + "    Using this command to upload a file.")
        print("-buy [hash]" + "    Using this command to buy a item.")
        print("-download [hash] [path]" + "    Using this command to download your own item to local.")
        args = input()
        argv = args.split()
        if len(argv) < 2:
            if len(argv) > 0 and argv[0] == "exit":
                close()
                print("goodbye~")
                break
            else:
                print(
                    "Wrong arguments! Please use the following command with arguments.\n" +
                    "-login [username]\n" +
                    "-add [filepath]\n" +
                    "-buy [hash]\n" +
                    "-download [hash] [path]"
                )
        else:
            main(argv, user, ipfs, bc, lshv)

        print("press enter to continue...")
        input()
        os.system("clear")


def isLogin(user):
    if user.curUser is None:
        print("You must login first to use this command!")
        print("-login [username]    Using this command to login.")
        return False
    return True


def permitDownload(user, block):
    if isLogin(user) and user.curUser == block.getFileOwner():
        return True
    return False


def initLSHVerify(blocks, ipfs):
    texts = []
    filenames = []
    for block in blocks.values():
        texts.append(ipfs.textContent(block.getIpfsAddr()))
        filenames.append(block.getFileName())

    lshv = LSHVerify(texts, filenames)
    return lshv


def clearLSHVerify():
    folderPath = os.path.join(os.getcwd(), "lshData")
    if os.path.exists(folderPath):
        for fn in os.listdir(folderPath):
            fp = os.path.join(folderPath, fn)
            if os.path.isfile(fp):
                os.remove(fp)


def close(user, ipfs):
    clearLSHVerify()
    user.close()
    ipfs.close()


if __name__ == '__main__':
    blocks = BlockChain()
    bcUser = User()
    bcIpfs = IpfsClient()

    historyItems = bcUser.getAllItems()
    for item in historyItems:
        ipfsObj = [{'Hash': item[0], 'Name': item[1], 'Size': str(item[2])}]
        blocks.addBlock(ipfsObj, item[4], item[3])

    homepage(bcUser, bcIpfs, blocks)
