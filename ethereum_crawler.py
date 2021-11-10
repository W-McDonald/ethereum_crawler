#!/usr/bin/env python3
import sys
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import logging
import itertools


class EtherscanCrawler(object):

    def __init__(self):
        self._init_logger()
        self.api_key = self._get_api_key()
        self.addresses = self._get_ethereum_addresses()
        self.base_url = 'https://api.etherscan.io/api?apikey={}'.format(self.api_key)

    def _init_logger(self):
        self._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def _get_api_key(self):
        with open('etherscan_api_key') as keyfile:
            LOG('GET: Ethereum API Key')
            return keyfile.readline().replace('\n', '')

    def _get_ethereum_addresses(self):
        LOG('GET: Ethereum Address DataFrame')
        return pd.read_csv('ethereum_addresses.csv')

    def __get_transactions_for_wallet(self, wallet):
        r = requests.get(url)
        LOG('GET:\n' + str(json.loads(r.content)))
        return json.loads(r.content)


if __name__ == '__main__':

    scanner = EtherscanCrawler()
    print(vars(scanner))
