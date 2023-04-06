import random
from automator.utils import EthDeFi
from web3 import Web3

CONTRACTS = {
    'bsc': {
        'busd': '0x98e871aB1cC7e3073B6Cc1B661bE7cA678A33f7F',
        'usdt': '0x0551ca9e33bada0355dfce34685ad3b73cf3ad70',
        'usdc': '0x8d1ebcda83fd905b597bf6d3294766b64ecf2aa7'
    }
}


class Harmony(EthDeFi):

    def get_harmony_contract(self, token):
        addr = self.w3.to_checksum_address(CONTRACTS[self.network][token])
        return self.get_contract(addr, 'harmony')

    def approve_token_for_me(self, token, amount):
        return self.approve_token(token, CONTRACTS[self.network][token], amount)

    def my_token_allowance(self, token):
        return self.token_allowance(token, CONTRACTS[self.network][token])

    def bridgeFromBsc(self, token, amount):
        self.approve_token_for_me(token, amount)
        harmonyChain = 116
        adapter_params = '0x0001000000000000000000000000000000000000000000000000000000000007a120'
        addr_as_bytes = self.wallet.ethAddr().lower()
        zeroAddr = self.w3.to_checksum_address('0x0000000000000000000000000000000000000000')
        contract = self.get_harmony_contract(token)
        tx = contract.functions.sendFrom(self.my_address(), harmonyChain, addr_as_bytes, amount,
                                         self.my_address(), zeroAddr, adapter_params).transact({
                                             'value':
                                             6034404505536,
                                             'from':
                                             self.my_address()
                                         })
        return self.w3.to_hex(tx)
