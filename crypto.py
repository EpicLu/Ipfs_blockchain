import base64
import rsa
import os


class Crypto:
    def __init__(self, user):
        self._pubkey = None
        self._prikey = None
        self.initCrypto(user)

    def initCrypto(self, user):
        folderPath = os.path.join(os.getcwd(), "token")
        wholePath = os.path.join(folderPath, f"{user}")
        pubkeyPath = os.path.join(wholePath, 'public.pem')
        prikeyPath = os.path.join(wholePath, 'private.pem')

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        if not os.path.exists(wholePath):
            os.makedirs(wholePath)

            (self._pubkey, self._prikey) = rsa.newkeys(1024)
            with open(pubkeyPath, 'w+') as f:
                f.write(self._pubkey.save_pkcs1().decode())
            with open(prikeyPath, 'w+') as f:
                f.write(self._prikey.save_pkcs1().decode())
            return

        with open(pubkeyPath, 'r') as f:
            self._pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        with open(prikeyPath, 'r') as f:
            self._prikey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    def encrypt(self, data):
        ret = rsa.encrypt(data.encode('utf-8'), self._pubkey)
        encrypted_base64 = base64.b64encode(ret).decode('utf-8')
        # print('pub encode:', crypto)
        return encrypted_base64

    def decrypt(self, encrypted_base64):
        try:
            encrypted = base64.b64decode(encrypted_base64.encode('utf-8'))
            data = rsa.decrypt(encrypted, self._prikey).decode()
            # print('pri decode:', data)
            return data
        except rsa.pkcs1.DecryptionError:
            # print("Insufficient permissions!")
            return None




