import mysql.connector
import hashlib
from crypto import Crypto
from datetime import datetime


class User:
    def __init__(self):
        config = {
            'user': 'EpicLu',
            'password': 'abcd1234',
            'host': 'localhost',
            'database': 'chainblock',
            'raise_on_warnings': True
        }

        self._cnx = mysql.connector.connect(**config)
        self.curUser = None
        self.token = None
        self._tradehash = None
        self._tradeCid = None

        cursor = self._cnx.cursor()
        queryTableUsers = "SHOW TABLES LIKE 'users'"
        cursor.execute(queryTableUsers)
        if not cursor.fetchone():
            createTableUsers = "CREATE TABLE users (username VARCHAR(50) PRIMARY KEY, pwd VARCHAR(50) NOT NULL)"
            cursor.execute(createTableUsers)
            cursor.fetchall()

        queryTableItems = "SHOW TABLES LIKE 'items'"
        cursor.execute(queryTableItems)
        if not cursor.fetchone():
            createTableItems = (
                "CREATE TABLE items ( \
                ipfsAddr VARCHAR(255) NOT NULL, \
                item VARCHAR(255) NOT NULL, \
                size BIGINT NOT NULL, \
                timestamp BIGINT NOT NULL, \
                owner VARCHAR(50) NOT NULL)"
            )
            cursor.execute(createTableItems)
            cursor.fetchall()

        queryTableTrades = "SHOW TABLES LIKE 'trades'"
        cursor.execute(queryTableTrades)
        if not cursor.fetchone():
            createTableTrades = (
                "CREATE TABLE trades ( \
                tradehash VARCHAR(255) NOT NULL, \
                blockhash VARCHAR(255) NOT NULL, \
                item VARCHAR(255) NOT NULL, \
                buyer VARCHAR(50) NOT NULL, \
                owner VARCHAR(50) NOT NULL, \
                timestamp BIGINT NOT NULL, \
                success BOOLEAN NOT NULL)"
            )
            cursor.execute(createTableTrades)
            cursor.fetchall()

        cursor.execute(queryTableUsers)
        if not cursor.fetchone():
            cursor.close()
            self.close()
            print("users table init failed...")
            exit(0)
        cursor.execute(queryTableItems)
        if not cursor.fetchone():
            cursor.close()
            self.close()
            print("items table init failed...")
            exit(0)
        cursor.execute(queryTableTrades)
        if not cursor.fetchone():
            cursor.close()
            self.close()
            print("items table init failed...")
            exit(0)
        cursor.close()

    def login(self, username, pwd):
        cursor = self._cnx.cursor()
        queryTableUsers = f"SELECT pwd FROM users WHERE username = '{username}'"
        cursor.execute(queryTableUsers)
        res = cursor.fetchall()
        cursor.close()
        if res:
            for data in res:
                if data[0] == pwd:
                    self.curUser = username
                else:
                    print("Password error!")
                    return
        else:
            self.registerUser(username, pwd)
        self.token = Crypto(username)
        print(f"welcome {self.curUser}")

    def registerUser(self, username, pwd):
        cursor = self._cnx.cursor()
        insertNewUser = f"INSERT INTO users (username, pwd) VALUES ('{username}', '{pwd}')"

        try:
            cursor.execute(insertNewUser)
            self._cnx.commit()
        except mysql.connector.Error:
            self._cnx.rollback()
            cursor.close()
            self.close()
            print(f"login has failed!")
            exit(0)

        self.curUser = username
        cursor.close()

    def saveItem(self, ipfsObj, timestamp):
        cursor = self._cnx.cursor()
        insertableItems = \
            f"INSERT INTO items SET \
                ipfsAddr = '{ipfsObj['Hash']}', \
                item = '{ipfsObj['Name']}', \
                size = '{ipfsObj['Size']}', \
                timestamp = {timestamp}, \
                owner = '{self.curUser}'"

        try:
            cursor.execute(insertableItems)
            self._cnx.commit()
        except mysql.connector.Error:
            self._cnx.rollback()
            cursor.close()
            self.close()
            print(f"saveItem has failed!")
            exit(0)
        cursor.close()

    def getAllItems(self):
        cursor = self._cnx.cursor()
        queryTableWorks = f"SELECT * FROM items"
        cursor.execute(queryTableWorks)
        res = cursor.fetchall()
        cursor.close()
        return res

    def transferItem(self, cid, owner):
        self._tradeCid = cid
        deCid = Crypto(owner).decrypt(cid)
        if deCid:
            newCid = self.token.encrypt(deCid)
            return newCid

    def recordTrade(self, cid, blockhash, item, buyer, owner):
        timestamp = int(datetime.utcnow().timestamp())
        message = str(cid) + str(timestamp)
        tradehash = hashlib.sha256()
        tradehash.update(message.encode('utf-8'))
        self._tradehash = tradehash.hexdigest()
        cursor = self._cnx.cursor()

        insertableTrades = \
            f"INSERT INTO trades SET \
                    tradehash = '{self._tradehash}', \
                    blockhash = '{blockhash}', \
                    item = '{item}', \
                    buyer = '{buyer}', \
                    owner = '{owner}', \
                    timestamp = {timestamp}, \
                    success = false"

        try:
            cursor.execute(insertableTrades)
            self._cnx.commit()
        except mysql.connector.Error:
            self._cnx.rollback()
            cursor.close()
            self.close()
            print(f"gen bill failed!")
            exit(0)
        cursor.close()

    def tradeCommit(self, cid):
        cursor = self._cnx.cursor()

        try:
            updateSuccess = f"UPDATE trades SET success = true WHERE tradehash = '{self._tradehash}'"
            cursor.execute(updateSuccess)
            self._cnx.commit()
            updateOwner = f"UPDATE items SET owner = '{self.curUser}', ipfsAddr = '{cid}' \
                WHERE ipfsAddr = '{self._tradeCid}'"
            cursor.execute(updateOwner)
            self._cnx.commit()
            cursor.close()
            self._tradehash = None
            self._tradeCid = None
            return True
        except mysql.connector.Error:
            self._cnx.rollback()
            print(f"bill update failed!")
            return False

    def close(self):
        self._cnx.close()

    # def test(self):
    # cursor = self._cnx.cursor()
    # queryTableWorks = f"SELECT * FROM users"
    # cursor.execute(queryTableWorks)
    # res = cursor.fetchall()
    # cursor.close()
    # return res

# u = User()
# u.login("test")
# for row in u.test():
#   print(row)
