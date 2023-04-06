import json
from automator.utils.utils import round_wei
from automator.utils.protostar import Protostar

CONTRACT_ADDR = "0xae0Ee0A63A2cE6BaeEFFE56e7714FB4EFE48D419"

info = {
    "ETH": {
        "l2_token_address": "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
        "l2_bridge_address": "0x073314940630fd6dcda0d772d4c972c4e0a9946bef9dabf4ef84eda8ef542b82"
    }
}


class StarkgateBridge:

    def deposit(w3, wallet, amount):
        f = open('./config/abi/eth_stark_bridge.json')
        abi = json.load(f)
        f.close()

        bridge = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        ethAmount = w3.from_wei(amount, 'ether')
        starkAddrInt = int(wallet.starkAddr(), base=16)
        print(f'Sending {ethAmount}eth to stark {wallet.starkAddr()}')
        tx_hash = bridge.functions.deposit(starkAddrInt).transact({
            "from": wallet.ethAddr(),
            "value": amount
        })
        return w3.to_hex(tx_hash)

    def initiateWithdraw(wallet, amount):
        protostar = Protostar(wallet)
        bridge = protostar.contract(info["ETH"]["l2_bridge_address"])
        bridge.function('initiate_withdraw').invoke([wallet.ethAddr(), amount,
                                                     0])  #uint256(amount,0)

    def completeWithdraw(w3, wallet):
        return
