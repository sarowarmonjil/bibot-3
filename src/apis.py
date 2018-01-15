# coding: utf-8
# https://github.com/huobiapi/API_Docs/wiki
import time
import urllib

import requests

import settings
import utils
from utils import sign, to_decimal


BTC = 'btcusdt'
ETH = 'ethusdt'
EOS = 'eosusdt'
ZEC = 'zecusdt'
_1MIN = '1min'
_5MIN = '5min'
_15MIN = '15min'
_30MIN = '30min'
_60MIN = '60min'

SYMBOLS = [BTC, ETH, EOS, ZEC]
PERIODS = [_1MIN, _5MIN, _15MIN, _30MIN, _60MIN]


def get_interval(symbol=BTC, period=_1MIN, size=300):
    # https://github.com/huobiapi/API_Docs/wiki/REST-Interval
    assert size > 0
    if size > 2000:
        print 'Warning: The size should be less than or equal to 2000'
    url = 'https://api.huobi.pro/market/history/kline'
    r = requests.get(url, {'symbol': symbol, 'period': period, 'size': size})
    return r.json()['data']


def post(method=None, extra_data=None, **kws):
    params = {
        'access_key': settings.AKEY,
        'secret_key': settings.SKEY,
        'created': int(time.time()),
        'method': method,
    }
    params.update(kws)
    signature = sign(params)
    params['sign'] = signature
    params.pop('secret_key')
    # 额外数据不参与签名
    if extra_data:
        for k, v in extra_data.iteritems():
            if v:
                params[k] = v

    payload = urllib.urlencode(params)
    r = requests.post(settings.HOST, params=payload)
    # 错误处理[摊手]
    assert r.status_code == 200
    r = r.json()
    kws = ', '.join('%s=%s' for k, v in kws.iteritems())
    assert 'code' not in r, '%s(%s) => %d %s' % (method, kws, r['code'], r['message'])
    utils.info('%s(%s) => %r', method, kws, r)
    return r


def get_account_info():
    return post('get_account_info')


def buy(coin_type, price, amount, trade_password=None, trade_id=None):
    price = to_decimal(price, 2)
    amount = to_decimal(amount, 2)
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('buy', price=price, coin_type=coin_type, amount=amount, extra_data=extra_data)


def buy_market(coin_type, amount, trade_password=None, trade_id=None):
    amount = to_decimal(amount, 2)  # amount的单位是元
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('buy_market', coin_type=coin_type, amount=amount, extra_data=extra_data)


def cancel_order(coin_type, id):
    return post('cancel_order', coin_type=coin_type, id=id)


def get_new_deal_orders(coin_type=BTC):
    return post('get_new_deal_orders', coin_type=coin_type)


def get_order_id_by_trade_id(coin_type, trade_id):
    return post('get_order_id_by_trade_id', coin_type=coin_type, trade_id=trade_id)


def get_orders(coin_type=BTC):
    return post('get_orders', coin_type=coin_type)


def get_order_info(coin_type, id):
    return post('order_info', coin_type=coin_type, id=id)


def sell(coin_type, price, amount, trade_password=None, trade_id=None):
    price = to_decimal(price, 2)
    amount = to_decimal(amount, 4)
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('sell', price=price, coin_type=coin_type, amount=amount, extra_data=extra_data)


def sell_market(coin_type, amount, trade_password=None, trade_id=None):
    amount = to_decimal(amount, 4)  # amount的单位是数字货币个数
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('sell_market', coin_type=coin_type, amount=amount, extra_data=extra_data)


if __name__ == '__main__':
    print get_interval()
    # print get_account_info()
    # print sell(BTC, 30000, 0.001)   # 4523039042L
    # print get_orders()
    # print get_new_deal_orders()
    # print get_order_info(BTC, 4523039042)
