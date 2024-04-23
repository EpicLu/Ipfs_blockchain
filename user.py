import mysql.connector


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

        cursor = self._cnx.cursor()
        queryTableUsers = "SHOW TABLES LIKE 'users'"
        cursor.execute(queryTableUsers)
        if not cursor.fetchone():
            createTableUsers = "CREATE TABLE users (username VARCHAR(50) PRIMARY KEY)"
            cursor.execute(createTableUsers)
            cursor.fetchall()

        queryTableItems = "SHOW TABLES LIKE 'items'"
        cursor.execute(queryTableItems)
        if not cursor.fetchone():
            createTableItems = (
                "CREATE TABLE items ( \
                ipfsAddr VARCHAR(255) PRIMARY KEY, \
                item VARCHAR(255) NOT NULL, \
                size BIGINT NOT NULL, \
                timestamp BIGINT NOT NULL, \
                owner VARCHAR(50) NOT NULL)"
            )
            cursor.execute(createTableItems)
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
        cursor.close()

    def login(self, username):
        cursor = self._cnx.cursor()
        queryTableUsers = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(queryTableUsers)
        res = cursor.fetchall()
        cursor.close()
        if res:
            self.curUser = username
        else:
            self.registerUser(username)
        print(f"welcome {self.curUser}")

    def registerUser(self, username):
        cursor = self._cnx.cursor()
        insertNewUser = f"INSERT INTO users (username) VALUES ('{username}')"

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
            ipfsAddr = '{ipfsObj[0]['Hash']}', \
            item = '{ipfsObj[0]['Name']}', \
            size = '{ipfsObj[0]['Size']}', \
            timestamp = '{timestamp}', \
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

    def transferItem(self, cid, buyer):
        cursor = self._cnx.cursor()

        try:
            updateOwner = f"UPDATE items SET owner = '{buyer}' WHERE ipfsAddr = '{cid}'"
            cursor.execute(updateOwner)
            self._cnx.commit()
        except mysql.connector.Error:
            self._cnx.rollback()
            return False
        cursor.close()
        return True

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
