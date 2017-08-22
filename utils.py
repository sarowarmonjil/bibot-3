# coding: utf-8
import time


def to_timestamp(datetime):
    return time.mktime(time.strptime(datetime, '%Y%m%d%H%M00000'))
