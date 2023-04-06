import json

ROUND_TO = 1000000000000000


class EthDeFi:
    ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    Tokens = {
        "arbitrum": {
            "usdt": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
        },
        "bsc": {
            "busd": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
            "usdt": "0x55d398326f99059fF775485246999027B3197955",
            "usdc": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
        }
    }

    def __init__(self, network, w3, wallet):
        self.network = network.lower()
        self.w3 = w3
        self.wallet = wallet

    def int_to_decimal(qty, decimal):
        return int(qty * int("".join(["1"] + ["0"] * decimal)))

    def decimal_to_int(price, decimal):
        return price / int("".join((["1"] + ["0"] * decimal)))

    def round_wei(amount):
        return int(amount / ROUND_TO) * ROUND_TO

    def get_token_address(self, token):
        token = token.lower()
        if token.startswith('0x'):
            return token
        if token == 'eth':
            return EthDeFi.ETH
        return EthDeFi.Tokens[self.network][token]

    def get_erc20_abi(self):
        file_name = f'{self.network}_erc20.json'
        f = open(f'./config/abi/{file_name}')
        abi = json.load(f)
        f.close()
        return abi

    def get_token_contract(self, token):
        address = self.get_token_address(token)
        return self.get_contract(address, 'erc20')

    def get_contract(self, address, name):
        file = f'./config/abi/{self.network}_{name}.json'
        f = open(file)
        abi = json.load(f)
        f.close()
        return self.w3.eth.contract(address=address, abi=abi)

    def my_address(self):
        return self.w3.to_checksum_address(self.wallet.ethAddr())

    def approve_token(self, token, spender, amount):
        spender = self.w3.to_checksum_address(spender)
        contract = self.get_token_contract(token)
        allowance = contract.functions.allowance(self.my_address(), spender).call()
        if allowance >= amount:
            return
        tx_hash = contract.functions.approve(spender, amount).transact({'from': self.my_address()})
        return self.w3.to_hex(tx_hash)

    def token_allowance(self, token, spender):
        spender = self.w3.to_checksum_address(spender)
        contract = self.get_token_contract(token)
        allowance = contract.functions.allowance(self.my_address(), spender).call()
        return allowance

    def convert_token_amount(self, token, amount):
        contract = self.get_token_contract(token)
        decimals = int(contract.functions.decimals().call())
        return EthDeFi.int_to_decimal(amount, decimals)

    def transfer_token(self, token, amount, to):
        contract = self.get_token_contract(token)
        to = self.w3.to_checksum_address(to)
        tx_hash = contract.functions.transfer(to, amount).transact({'from': self.my_address()})
        return self.w3.to_hex(tx_hash)

    def token_balance(self, token):
        addr = self.w3.to_checksum_address(self.my_address())
        contract = self.get_token_contract(token)
        balance = int(contract.functions.balanceOf(addr).call())
        return balance

    def converted_token_balance(self, token):
        contract = self.get_token_contract(token)
        decimals = int(contract.functions.decimals().call())
        balance = self.token_balance(token)
        return EthDeFi.decimal_to_int(balance, decimals)
