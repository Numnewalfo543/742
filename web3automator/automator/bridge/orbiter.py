import random
from automator.utils import EthDeFi

info = {
    "arbitrum_eth":
    ["0x80c67432656d59144ceff962e8faf8926599bcf8", "0xe4edb277e41dc89ab076a1f049f4a3efa700bce8"],
    "arbitrum_usdt": ["0xd7Aa9ba6cAAC7b0436c91396f22ca5a7F31664fC"],
    "arbitrum_usdc": []
}

codes = {"polygon": 9006, "optimism": 9007, "zkera": 9014}


class Orbiter(EthDeFi):

    def _get_bridge(self, name):
        addr = random.choice(info[name])
        return self.w3.to_checksum_address(addr)

    #0.001ETH will be withholded
    def depositZkEra(self, amount):
        return self._deposit(amount, "zkera")

    def depositOptimism(self, amount):
        return self._deposit(amount, "optimism")

    def depositPolygon(self, amount):
        return self._deposit(amount, "polygon")

    def depositErc20(self, token, amount, target):
        amount = amount + codes[target]
        fromName = self.network + "_" + token
        bridge = self._get_bridge(fromName)
        return self.transfer_token(token, amount, bridge)

    def _deposit(self, amount, toName):
        fromName = self.network + "_eth"
        amount = amount + codes[toName]
        bridge = self._get_bridge(fromName)
        tx_hash = self.w3.eth.send_transaction({
            'to': bridge,
            'from': self.wallet.ethAddr(),
            'value': amount
        })
        print(f'Bridging from {fromName} to {toName} for {amount}wei')
        return self.w3.to_hex(tx_hash)