from automator.utils import WalletProvider, EthDeFi
from automator.utils import round_wei, wait_for_gas
import time
from decimal import Decimal
from automator.exchanger.one_inch import OneInch
from automator.bridge import Harmony, Core
from automator.utils import EthDeFi
import random
import requests


def swap_to_bnb(w3, wallet, token):
    oneInch = OneInch("bsc", w3, wallet)
    amount = oneInch.convert_token_amount(token, 6)
    tx = oneInch.exchange(token.upper(), EthDeFi.ETH, amount)
    print(tx)
    time.sleep(50)


def swap_from_bnb(w3, wallet, token, l0config):
    ca = l0config['bnb_swap']
    print("Swap from BNB")
    oneInch = OneInch("bsc", w3, wallet)
    amount = w3.to_wei(Decimal(random.uniform(ca[0], ca[1])), 'ether')
    tx = oneInch.exchange(EthDeFi.ETH, token.upper(), amount)
    print(f'swap {amount}: {tx}')
    time.sleep(50)


def validate_code(code):
    x = requests.get(f'https://blockside.planemostd.com/amount_left?code={code}')
    print(f'Bridges left: {x.text}')
    if int(x.text) <= 0:
        print("No more transactions left")
        raise Exception("No more transactions left")
    return


def consume_code(code):
    x = requests.post(f'https://blockside.planemostd.com/consume?code={code}')
    return


def perform(wallet, w3, config):
    l0config = config['l0']
    bnbBalance = w3.eth.get_balance(wallet.ethAddr())
    if bnbBalance < 100:
        print(f"Low balance: {bnbBalance}")
        raise Exception("Low balance")

    defi = EthDeFi('bsc', w3, wallet)

    token = ''
    balance = 0
    balanceUsdc = defi.token_balance('usdc')
    balanceUsdt = defi.token_balance('usdt')
    if balanceUsdc > 0:
        balance = balanceUsdc
        token = 'usdc'
    elif balanceUsdt > 0:
        balance = balanceUsdt
        token = 'usdt'
    else:
        token = random.choice(['usdc', 'usdt'])

    tka = l0config['token_bridge_cents']
    amount = defi.convert_token_amount(token, random.randint(tka[0], tka[1]) / 100)
    print(amount)

    if balance < amount:
        swap_from_bnb(w3, wallet, token, l0config)
        time.sleep(random.randint(10, 50))
        balance = defi.token_balance(token)

    print(f'Balance: {bnbBalance}bnb  {balance}{token}')

    #swap_to_bnb(w3, wallet, token)

    def do_harmony():
        harmony = Harmony('bsc', w3, wallet)
        allowance = harmony.my_token_allowance(token)
        print(f'Harmony allowance: {allowance} required {amount}')
        if allowance < amount:
            tx = harmony.approve_token_for_me(token, amount * 11)
            print(f'Set token allowance: {tx}')
            time.sleep(random.randint(30, 90))

        tx = harmony.bridgeFromBsc(token, amount)
        print(f'harmony {tx}')

    def do_core():
        core = Core('bsc', w3, wallet)
        allowance = core.my_token_allowance(token)
        print(f'Core allowance: {allowance} required {amount}')
        if allowance < amount:
            tx = core.approve_token_for_me(token, amount * 11)
            print(f'Set token allowance: {tx}')
            time.sleep(random.randint(30, 90))

        tx = core.bridgeFromBsc(token, amount)
        print(f'core {tx}')

    if random.randrange(2) == 0:
        do_harmony()
    else:
        do_core()


def do_all():
    walletProvider = WalletProvider("./wallets/wallets.json", './config/config.json')
    walletProvider.shuffle()
    for wallet in walletProvider:
        code = walletProvider.config['code']
        validate_code(code)
        try:
            w3 = walletProvider.getWeb3WithWallet('bsc', wallet)
            perform(wallet, w3, walletProvider.config)
            consume_code(code)
        except:
            print('An exception occured, trying next wallet')
        cd = walletProvider.config['l0']['delays']
        time.sleep(random.randint(cd[0], cd[1]))


do_all()