from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3 import Web3


def node_default_gas_price_strategy(web3: Web3, transaction_params: dict) -> int:
    node_default_price = rpc_gas_price_strategy(web3)
    return node_default_price