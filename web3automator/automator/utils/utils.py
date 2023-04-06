import time

ROUND_TO = 1000000000000000


def round_wei(amount):
    return int(amount / ROUND_TO) * ROUND_TO


def wait_for_gas(w3, targetGasPrice):
    while True:
        gasPrice = w3.eth.gas_price
        if gasPrice <= targetGasPrice:
            break
        print(f'Waiting: current gas price is {gasPrice}')
        time.sleep(10)

