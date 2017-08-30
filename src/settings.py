# coding: utf-8
import os

import envs


def getenv(key, default=None):
    return os.getenv(key) or getattr(envs, key, default)


DATABASE = {
    'NAME': getenv('DB_NAME', 'db.sqlite'),
}


AKEY = getenv('AKEY')
SKEY = getenv('SKEY')
HOST = getenv('HOST', 'https://api.huobi.com/apiv3')


(ALL, DEBUG, INFO, ERROR, QUIET) = range(5)
LOG_LEVEL = getenv('LOG_LEVEL', INFO)


def can_print(level):
    return level >= LOG_LEVEL
