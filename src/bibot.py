# coding: utf-8
import time

from ta import _get_test_data
from strategies import Policy
import apis
import utils


def bibot_v1():
    data = apis.get_account_info()
    balance = float(data['available_cny_display'])
    amount = float(data['available_btc_display'])

    closing, values = _get_test_data()
    p = Policy()
    p.load()
    c = p(values[-1:])[0]
    if c == 1 and balance >= 500:
        print utils.now(), 'buy'
        apis.buy_market(apis.BTC, '500.00')
    elif c == 0 and amount >= 0.0010:
        print utils.now(), 'sell'
        apis.sell_market(apis.BTC, amount)


def bibot_v2():
    data = apis.get_account_info()
    balance = float(data['available_cny_display'])
    amount = float(data['available_btc_display'])
    price = apis.get_interval(length=1)[0][4]
    if price >= 32250 or price <= 27250:
        apis.sell_market(apis.BTC, amount)
        exit(0)

    orders = apis.get_orders()
    orders = {o['order_price']: o for o in orders}

    pointer = int(round((price - 27000.) / 500.) * 500 + 27000)
    if utils.to_decimal(pointer, 2) in orders:
        return

    for price in range(pointer + 500, 32500, 500):
        price = utils.to_decimal(price, 2)
        if price not in orders and amount > 0.0035:
            apis.sell(apis.BTC, price, 0.0035)
            amount -= 0.0035

    for price in range(pointer - 500, 27000, -500):
        price = utils.to_decimal(price, 2)
        if price not in orders and balance > 112:
            apis.buy(apis.BTC, price, 0.0035)
            balance -= 112

if __name__ == '__main__':
    while True:
        time.sleep(5)
        bibot_v2()
