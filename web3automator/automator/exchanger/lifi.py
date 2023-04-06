from automator.utils import EthDeFi
import requests
import time


class LiFi(EthDeFi):

    def exchange(self, fromToken, toToken, amount):
        return