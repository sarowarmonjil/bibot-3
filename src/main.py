#! /usr/bin/env python
# coding: utf-8
# https://www.huobi.com/
import time
from pprint import pprint

import apis
import orm
import utils
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
    elif args.cmd == 'show':
        pprint(apis.get_account_info())
    elif args.cmd == 'sim':
        from strategies import Policy
        from ta import _get_test_data
        import matplotlib.pyplot as plt

        close, features = _get_test_data()
        p = Policy()
        p.load()
        d = p(features)
        print utils.simulate(zip(d, close))

        fig, ax1 = plt.subplots()
        ax1.plot(close, 'b-')
        ax1.set_xlabel('time (s)')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('price', color='b')
        ax1.tick_params('p', colors='b')

        last = 0
        data = []
        for c in d:
            if c == 2:
                c = last
            data.append(c)
            last = c

        ax2 = ax1.twinx()
        ax2.plot(d, 'r-')
        ax2.set_ylabel('vol', color='r')
        ax2.tick_params('v', color='r')

        fig.tight_layout()
        plt.show()

'''
一个好的策略是：

1. 设下止损位；（10%）
1. 该策略应该能避免频繁买卖，且该策略中不存在对买卖频率的直接限制。
1. 避免限价出入市，要在市场中买卖。
1. 在市场趋势不明显时，在场外观望。
1. 只在活跃的市场买卖，买卖清淡时不宜操作。
（1）将你的资本分为十份，每次入市买卖，损失不会超过资本的十分之一；
（3）不可过量买卖；
（4）不让所持仓位由盈转亏；
（8）可用止损位保障所得利润。
（9）在市场中连战皆胜后，可将部分利润提出，以备急时之需。
（17）不要因为价位过低而吸纳，也不要因为价位过高而看空。
（18）避免在不适当的时候金字塔式加码。
（20）如无适当理由，避免胡乱更改所持仓位的买卖策略。
'''
