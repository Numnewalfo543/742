import random
from automator.utils import EthDeFi
from web3 import Web3

CONTRACTS = {'bsc': '0x52e75D318cFB31f9A2EdFa2DFee26B161255B233'}


class Core(EthDeFi):

    def get_core_contract(self):
        addr = self.w3.to_checksum_address(CONTRACTS[self.network])
        return self.get_contract(addr, f'core')

    def my_token_allowance(self, token):
        return self.token_allowance(token, CONTRACTS[self.network])

    def approve_token_for_me(self, token, amount):
        return self.approve_token(token, CONTRACTS[self.network], amount)

    def bridgeFromBsc(self, token, amount):
        self.approve_token_for_me(token, amount)
        adapter_params = '0x'
        zeroAddr = self.w3.to_checksum_address('0x0000000000000000000000000000000000000000')
        contract = self.get_core_contract()
        token_addr = self.w3.to_checksum_address(self.get_token_address(token))
        tx = contract.functions.bridge(token_addr, amount, self.my_address(),
                                       [self.my_address(), zeroAddr], adapter_params).transact({
                                           'value':
                                           85247655643584,
                                           'from':
                                           self.my_address()
                                       })
        return self.w3.to_hex(tx)
