# coding: utf-8
# http://docs.peewee-orm.com/en/latest/
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

import settings
import utils


db = SqliteExtDatabase(settings.DATABASE['NAME'])


BTC = 'btc'
COIN_TYPE = [
    (BTC, BTC),
]


DateTimeField = peewee.CharField


class CoinTypeField(peewee.CharField):
    def __init__(self, *args, **kws):
        kws['choices'] = COIN_TYPE
        return super(CoinTypeField, self).__init__(*args, **kws)


class KLine(peewee.Model):
    coin_type = CoinTypeField()
    period = peewee.IntegerField()
    started_at = DateTimeField()

    opening = peewee.FloatField()
    top = peewee.FloatField()
    bottom = peewee.FloatField()
    closing = peewee.FloatField()
    turnover = peewee.FloatField()

    class Meta:
        database = db
        indexes = [
            (('coin_type', 'period', 'started_at'), True),
        ]

    def create_or_nothing(self):
        try:
            super(KLine, self).save(force_insert=True)
        except peewee.IntegrityError:
            pass

    def save(self, force_insert, **kws):
        if force_insert:
            self.create_or_nothing()
        else:
            super(KLine, self).save(**kws)

    @staticmethod
    def get_latest_time():
        line = KLine.select().order_by(KLine.started_at.desc()).first()
        return line and utils.to_timestamp(line.started_at)


def create_kline(coin_type, period, line):
    KLine.create(coin_type=coin_type,
                 period=period,
                 started_at=line[0],
                 opening=line[1],
                 top=line[2],
                 bottom=line[3],
                 closing=line[4],
                 turnover=line[5])


db.connect()
# https://github.com/coleifer/peewee/issues/211
KLine.create_table(fail_silently=True)
