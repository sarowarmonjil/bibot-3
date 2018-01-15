#! /usr/bin/env python
# coding: utf-8
# https://www.huobi.com/
import itertools
from pprint import pprint

import apis
import orm
from arg import args


def _sync_kline(symbol, period):
    for line in apis.get_interval(symbol, period, 2000)[:-1]:
        orm.create_kline(symbol, period, line)


def sync_kline():
    for symbol, period in itertools.product(apis.SYMBOLS, apis.PERIODS):
        _sync_kline(symbol, period)


if __name__ == '__main__':
    if args.cmd == 'sync':
        sync_kline()
    elif args.cmd == 'show':
        pprint(apis.get_account_info())
