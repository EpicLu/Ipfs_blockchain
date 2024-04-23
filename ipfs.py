import ipfshttpclient


class IpfsClient:
    def __init__(self, addr='/ip4/127.0.0.1/tcp/5001/http'):
        self._client = ipfshttpclient.connect(addr)

    # def test(self):
        # return self.client.pin.ls()
        # return self.client.files.stat('QmbVWF3sdBQkFPxDWm6nbGBcbA6JmJn9C1hGhnaaUdXi2r')

    def upload(self, filepath, pattern=None, isDirectory=False):
        res = self._client.add(
            filepath,
            wrap_with_directory=True,
            pattern=pattern,
            recursive=isDirectory,
            pin=isDirectory)

        return res

    def download(self, cid, path='./download'):
        self._client.get(cid, path)

    def close(self):
        self._client.close()


# ipfs = IpfsClient()
# print(ipfs.upload('test.txt'))
# ipfs.download('QmbVWF3sdBQkFPxDWm6nbGBcbA6JmJn9C1hGhnaaUdXi2r')
# print(ipfs.test())
