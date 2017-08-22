# coding: utf-8
# https://github.com/huobiapi/API_Docs/wiki
import requests


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

if __name__ == '__main__':
    a = get_interval(BTC, 1, 2)
    print a
