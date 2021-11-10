#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import logging
from etherscan import Etherscan


class EthereumCrawler(object):

    def __init__(self, local_path='./', entities=None):
        self.logger = self._init_logger()
        self.api_key = self._get_api_key()
        self.etherscan = Etherscan(self.api_key)
        self.local_path = local_path
        self.entities = entities
        self.addresses = self._get_ethereum_addresses()

    def _init_logger(self):
        self._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)

    def _get_api_key(self):
        with open('api_key') as keyfile:
            self._logger.info('>>> Reading API Key')
            return keyfile.readline().replace('\n', '')

    def _parse_addresses_csv(self):
        addresses = pd.read_csv('addresses.csv')
        addresses['entity'] = addresses['entity'].apply(lambda x: x.lower().replace(' ', '_'))
        addresses['label'] = addresses['label'].apply(lambda x: x.lower().replace(' ', '_'))
        return addresses
        

    def _get_ethereum_addresses(self):
        all_entities = self._parse_addresses_csv()
        if not self.entities:
            self._logger.info('>>> Fetching All Ethereum Addresses')
            return all_entities
        else:
            self._logger.info('>>> Fetching Specified Ethereum Addresses')
            filtered_entities = all_entities.loc[all_entities['entity'].str.contains(self.entities, na=False)]
            return filtered_entities

    def _get_addresses_by_entity(self, partial_match=True):
        return None
    
    def _get_addresses_by_label(self, partial_match=True):
        return None

    def get_all_txs_for_addresses(self):
        for index, row in self.addresses.iterrows():
            self._logger.info('>>> Getting Transactions for Address of Entity: {}'.format(row['entity']))
            try:
                tx_df = pd.DataFrame(self.etherscan.get_normal_txs_by_address(row['address'], 0, 99999999, 'asc'))
                tx_df['entity'] = row['entity']
                tx_df['address'] = row['address']
                tx_df.to_csv(self.local_path + '{}.csv'.format(row['entity'], index=False))
            except:
                self._logger.error('>>> Unable to Get Transactions for Address of Entity: {}'.format(row['entity']))

