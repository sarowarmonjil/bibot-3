# coding: utf-8
import calendar
from datetime import datetime

import pytz


def to_timestamp(t):
    t = datetime.strptime(t, '%Y%m%d%H%M00000')
    t = t.replace(tzinfo=pytz.FixedOffset(480))     # 东八区
    return calendar.timegm(t.utctimetuple())        # utc timestamp
