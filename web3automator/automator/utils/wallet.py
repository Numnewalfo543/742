class Wallet:

    def __init__(self, data):
        self._data = data

    def name(self):
        return self._data['name']

    def ethAddr(self):
        return self._data['eth'][0]

    def ethPriv(self):
        return self._data['eth'][1]

    def starkAddr(self):
        return self._data['stark'][0]

    def starkPriv(self):
        return self._data['stark'][1]