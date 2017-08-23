# coding: utf-8
import os

import envs


def getenv(key, default=None):
    return os.getenv(key) or getattr(envs, key, default)


DATABASE = {
    'NAME': getenv('DB_NAME', 'db.sqlite')
}
