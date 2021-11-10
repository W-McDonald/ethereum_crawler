#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import os
from ethereum_crawler import EthereumCrawler
import argparse
import warnings
warnings.filterwarnings('ignore')


def get_args():

    def __validate_args(args):
        if not args.local_path:
            return parser.error('--local-path not specified')
        if not os.path.isdir(args.local_path):
            return parser.error('--local-path: {} does not exist'.format(args.local_path))
        else:
            if '~' in args.local_path:
                args.local_path = os.path.expanduser(args.local_path)
            
        return args

    parser = argparse.ArgumentParser(prog='ethereum_crawler', description='Crawl the Ethereum Blockchain via Etherscan for Data')
    parser.add_argument(
            '--local-path', dest='local_path', type=lambda x: '{}/'.format(str(x)).replace('//','/'), nargs='?',
            required=False, default=None, help="Optional local path to save csv output files"
        )
    parser.add_argument(
            '--run-continuously', dest='run_continuously', type=lambda x: bool(x), nargs='?',
            required=False, default=False, help="If True, this runs on repeat. Default = False."
        )
    parser.add_argument(
            '--entities', dest='entities', type=lambda x: str(x).replace(',','|'), nargs='?',
            required=False, default=None, help="One to many substrings separated by commas; returns api calls for all entities with names containing exact matches of substrings... e.g. '--entities coinbase,binance,crypto,exchange'' results in every entity which contains any of those four substrings"
        )
    return __validate_args(parser.parse_args())


def main():
    args = get_args()
    crawler = EthereumCrawler(args.local_path, args.entities)
    if args.run_continuously:
        while True:
            crawler.get_all_txs_for_addresses()
    else:
        crawler.get_all_txs_for_addresses()


if __name__ == '__main__':
    main()

