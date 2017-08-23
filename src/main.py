#! /usr/bin/env python
# coding: utf-8
# https://www.huobi.com/
import time

import apis
import orm
from arg import args


def sync_kline():
    last_time = orm.KLine.get_latest_time()
    if last_time:
        interval = int((time.time() - last_time) / 60)
    else:
        interval = 2000
    for line in apis.get_interval(apis.BTC, 1, interval + 10)[:-1]:
        orm.create_kline(orm.BTC, 1, line)

if __name__ == '__main__':
    if args.cmd == 'sync':
        sync_kline()
