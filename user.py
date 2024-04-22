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
        self.user = None

        cursor = self._cnx.cursor()
        queryTableUsers = "SHOW TABLES LIKE 'users'"
        cursor.execute(queryTableUsers)
        if not cursor.fetchone():
            createTableUsers = "CREATE TABLE users (username VARCHAR(50) PRIMARY KEY)"
            cursor.execute(createTableUsers)

        queryTableWorks = "SHOW TABLES LIKE 'works'"
        cursor.execute(queryTableWorks)
        if not cursor.fetchone():
            createTableWorks = (
                "CREATE TABLE works ( \
                work VARCHAR(255) NOT NULL, \
                owner VARCHAR(50) NOT NULL)"
            )
            cursor.execute(createTableWorks)

        cursor.execute(queryTableUsers)
        if not cursor.fetchone():
            print("user init failed...")
            cursor.close()
            exit(0)
        cursor.close()

    def login(self, username):
        cursor = self._cnx.cursor()
        queryTableUsers = f"SELECT username = '{username}' FROM users"
        cursor.execute(queryTableUsers)
        res = cursor.fetchone()
        if res[0] > 0:
            self.user = username
        else:
            self.registerUser(username)
        print(f"welcome {self.user}")
        cursor.close()

    def registerUser(self, username):
        cursor = self._cnx.cursor()
        insertNewUser = f"INSERT INTO users (username) VALUES ('{username}')"

        try:
            cursor.execute(insertNewUser)
            self._cnx.commit()
        except mysql.connector.Error:
            self._cnx.rollback()
            print(f"login has failed!")
            exit(0)

        self.user = username
        cursor.close()

    def getWorks(self):
        cursor = self._cnx.cursor()
        queryTableWorks = f"SELECT '{self.user}' FROM works"
        cursor.execute(queryTableWorks)
        res = cursor.fetchall()
        cursor.close()
        return res

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
