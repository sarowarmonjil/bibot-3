# coding: utf-8
import calendar
import hashlib
import itertools
import sys
import urllib
from datetime import datetime

import pytz

import settings


def to_timestamp(t):
    t = datetime.strptime(t, '%Y%m%d%H%M00000')
    t = t.replace(tzinfo=pytz.FixedOffset(480))     # 东八区
    return calendar.timegm(t.utctimetuple())        # utc timestamp


def now():
    t = datetime.now(pytz.FixedOffset(480))
    return t.strftime('%Y/%m/%d %H:%M:%S')


def sign(params):
    params = sorted(params.iteritems())
    msg = urllib.urlencode(params)
    return hashlib.md5(msg).hexdigest()


def to_decimal(number, places):
    if isinstance(number, (int, float)):
        fmt = '%%.%df' % places
        number = fmt % number
    return number


def _print(fp, level, fmt, *args):
    if settings.can_print(level):
        print >> fp, fmt % args


def info(fmt, *args):
    _print(sys.stdout, settings.INFO, fmt, *args)


def error(fmt, *args):
    _print(sys.stderr, settings.ERROR, fmt, *args)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def evaluate(items):
    balance = 0.
    amount = 0.
    for vol, closing in items:
        balance += 500.
        amount += 0.998 * 500. / closing
        if vol == 0:
            balance += 0.998 * amount * closing
            amount = 0.
        elif vol == 1:
            amount += 0.998 * balance / closing
            balance = 0.
    return (balance + 0.998 * closing * amount) / len(items)


def simulate(items):
    balance = 500.
    amount = 0.
    last = 0
    for vol, closing in items:
        if vol != 2 and vol != last:
            if vol == 0:
                balance = 0.9995 * amount * closing
                amount = 0.
            elif vol == 1:
                amount = 0.9995 * balance / closing
                balance = 0.
            last = vol
    return balance + closing * amount


if __name__ == '__main__':
    items = [(1., 28000), (2, 28500), (0, 29000)]
    print simulate(items)
