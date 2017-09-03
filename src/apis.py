# coding: utf-8
# https://github.com/huobiapi/API_Docs/wiki
import math
import time
import urllib

import requests

import settings
import utils
from utils import sign, to_decimal

BTC = 1
LTC = 2


def get_interval(coin_type=BTC, period=1, length=300):
    # https://github.com/huobiapi/API_Docs/wiki/REST-Interval
    assert length > 0
    if length > 2000:
        print 'Warning: The length should be less than or equal to 2000'
    coin_type = {BTC: 'btc', LTC: 'ltc'}[coin_type]
    url = 'https://api.huobi.com/staticmarket/%s_kline_%03d_json.js?length=%d'
    url = url % (coin_type, period, length)
    r = requests.get(url)
    return r.json()


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
    kws = ', '.join('%s=%s' % item for item in kws.iteritems())
    assert 'code' not in r, '%s(%s) => %d %s' % (method, kws, r['code'], r['message'])
    utils.info('%s(%s) => %r', method, kws, r)
    return r


def get_account_info():
    return post('get_account_info')


def buy(coin_type, price, amount, trade_password=None, trade_id=None):
    price = to_decimal(price, 2)
    amount = to_decimal(amount, 4)
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('buy', price=price, coin_type=coin_type, amount=amount, extra_data=extra_data)


def buy_market(coin_type, amount, trade_password=None, trade_id=None):
    # https://github.com/huobiapi/API_Docs/wiki/REST-buy_market
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
    amount = to_decimal(amount, 4)
    extra_data = {
        'trade_password': trade_password,
        'trade_id': trade_id,
    }
    return post('sell_market', coin_type=coin_type, amount=amount, extra_data=extra_data)


def smart_buy(coin_type, price, amount):
    if amount >= 0.0010:
        return buy(coin_type, price, amount)
    elif amount <= -0.0010:
        return sell(coin_type, price, math.fabs(amount))


def smart_buy_market(coin_type, cny):
    if cny > 30.:
        return buy_market(coin_type, cny)
    elif cny < -30.:
        return sell_market(coin_type, cny)


if __name__ == '__main__':
    print get_interval(BTC, 1, 2)
    print get_account_info()
    # print sell(BTC, 30000, 0.001)   # 4523039042L
    # print get_orders()
    # print get_new_deal_orders()
    # print get_order_info(BTC, 4523039042)
