from automator.utils import EthDeFi
import requests
import time


class OneInch(EthDeFi):
    CHAINS = {"arbitrum": 42161, "bsc": 56, "polygon": 137, "optimism": 10, "avalanche": 43114}
    API_VERSION = "v5.0"

    def exchange(self, fromToken, toToken, amount):
        if fromToken != EthDeFi.ETH and fromToken != 'ETH':
            spender = self.get_spener_address()
            self.approve_token(fromToken, spender, amount)
            time.sleep(10)
        apiUrl = self.build_url(fromToken, toToken, amount)
        tx = self.get_api_tx(apiUrl)
        tx['to'] = self.w3.to_checksum_address(tx['to'])
        tx['gasPrice'] = int(tx['gasPrice'])
        tx['value'] = int(tx['value'])
        tx_hash = self.w3.eth.send_transaction(tx)
        return self.w3.to_hex(tx_hash)

    def get_network_id(self):
        return OneInch.CHAINS[self.network]

    def get_spener_address(self):
        url = f'https://api.1inch.io/{OneInch.API_VERSION}/{self.get_network_id()}/approve/spender'
        try:
            call_data = requests.get(url)
            api_data = call_data.json()
            return api_data['address']
        except Exception as e:
            print(e)
        return None

    def build_url(self, fromToken, toToken, amount):
        networkId = self.get_network_id()
        addr = self.my_address()
        fromTokenAddr = self.get_token_address(fromToken)
        toTokenAddr = self.get_token_address(toToken)
        return f'https://api.1inch.io/{OneInch.API_VERSION}/{networkId}/swap?fromTokenAddress={fromTokenAddr}&toTokenAddress={toTokenAddr}&amount={amount}&fromAddress={addr}&slippage=1'

    def get_api_tx(self, url):
        try:
            call_data = requests.get(url)
        except Exception as e:
            print(e)
        try:
            api_data = call_data.json()
            return api_data['tx']
        except Exception as e:
            print(call_data.text)
