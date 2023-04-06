import os


class Protostar:

    def __init__(self, wallet):
        self.address = wallet.starkAddr()
        self.privateKey = wallet.starkPriv()

    def contract(self, contractAddress):
        return PContract(self, contractAddress)


class PContract:

    def __init__(self, protostar, address):
        self.protostar = protostar
        self.address = address

    def function(self, name):
        return PFunction(self, name)


class PFunction:

    def __init__(self, contract, name):
        self.contract = contract
        self.name = name

    def invoke(self, arguments):
        argsStr = ' '.join(arguments)
        os.environ["PROTOSTAR_ACCOUNT_PRIVATE_KEY"] = self.contract.protostar.privateKey
        command = f'protostar invoke --contract-address {self.contract.address} \
            --function "{self.name}" \
            --network mainnet \
            --account-address {self.contract.protostar.address} \
            --max-fee auto \
            --inputs {argsStr}'

        os.system(command)
