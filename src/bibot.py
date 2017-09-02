# coding: utf-8
import time

import numpy as np

from analysis import features
from strategies import Policy
import apis
import utils


def xxx(values):
    # d = 2 * np.ones(len(values))
    d = np.ones(len(values))
    # d[values[:, 0] >= 0] = 1
    # d[values[:, 0] <= ] = 0
    return d


if __name__ == '__main__':
    while True:
        time.sleep(1)

        data = apis.get_account_info()
        balance = float(data['available_cny_display'])
        amount = float(data['available_btc_display'])

        closing, values = features()
        p = Policy()
        p.load()
        c = p(values[-1:])[0]
        if c == 1 and balance >= 500:
            print utils.now(), 'buy'
            apis.buy_market(apis.BTC, '500.00')
        elif c == 0 and amount >= 0.0010:
            print utils.now(), 'sell'
            apis.sell_market(apis.BTC, amount)
