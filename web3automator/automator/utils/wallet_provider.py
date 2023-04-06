import json
import random
from web3 import Web3
from .wallet import Wallet
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware, geth_poa_middleware
from eth_account import Account
from .gas import node_default_gas_price_strategy


class WalletProvider:

    def __init__(self, filePath, configPath):
        self._wallets = []
        self._iterator = None
        self.config = None
        self.loadMoreWallets(filePath)
        self._loadConfig(configPath)

    def _loadConfig(self, filePath):
        with open(filePath) as f:
            self.config = json.load(f)

    def loadMoreWallets(self, filePath):
        with open(filePath) as f:
            wallets = json.load(f)
            wallets = [Wallet(w) for w in wallets]
            self._addWallets(wallets)

    def excludeWallets(self, addrs):

        def leave(wallet):
            return not (wallet.ethAddr() in addrs or wallet.starkAddr() in addrs)

        wallets = filter(leave, self._wallets)
        self._updateWallets(wallets)

    def _addWallets(self, wallets):
        self._wallets = self._wallets + wallets
        self._iterator = iter(self._wallets)

    def shuffle(self):
        random.shuffle(self._wallets)
        self._iterator = iter(self._wallets)

    def getRandomWallet(self):
        return next(self._iterator)

    def getWallet(self, number):
        return self._wallets[number]

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)

    def getConfig(self):
        return self.config

    def getWeb3WithWallet(self, network, wallet):
        w3 = Web3(Web3.HTTPProvider(self.config['network'][network]['rpc']))
        if not w3.is_connected():
            print("Error: connection error, try using different RPC")
        account: LocalAccount = Account.from_key(wallet.ethPriv())
        print('===============================')
        print(f'{wallet.name()}: {account.address}')
        #setup account
        if network == 'bsc':
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            w3.eth.set_gas_price_strategy(node_default_gas_price_strategy)
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account), 'local_wallet')
        w3.eth.defaultAccount = account.address
        return w3

    def getWeb3(self, network, walletNumber):
        wallet = self.getWallet(walletNumber)
        return self.getWeb3WithWallet(network, wallet)