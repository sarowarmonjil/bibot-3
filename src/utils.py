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
