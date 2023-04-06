import json
from automator.utils.utils import round_wei

CONTRACT_ADDR = "0xaBEA9132b05A70803a4E85094fD0e1800777fBEF"


class ZkLiteBridge:

    def bridgeEthToZkLite(w3, wallet, amount):
        f = open('automator/system/eth_zklite_bridge_abi.json')
        abi = json.load(f)
        f.close()

        bridge = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        ethAmount = w3.from_wei(amount, 'ether')
        print(f'Sending {ethAmount}eth to zkLite {wallet.ethAddr()}')
        tx_hash = bridge.functions.depositETH(wallet.ethAddr()).transact({
            "from": wallet.ethAddr(),
            "value": amount
        })
        return w3.to_hex(tx_hash)
