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


class Order(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    order_time = peewee.IntegerField()
    type = peewee.SmallIntegerField()                           # 1限价买　2限价卖　3市价买　4市价卖
    order_price = peewee.DecimalField(decimal_places=2)         # 委托价格
    order_amount = peewee.DecimalField(decimal_places=4)        # 委托数量
    processed_price = peewee.DecimalField(decimal_places=2)     # 成交平均价格
    processed_amount = peewee.DecimalField(decimal_places=4)    # 已经完成的数量
    vot = peewee.DecimalField(decimal_places=2)                 # 交易额
    fee = peewee.DecimalField(decimal_places=2)                 # 手续费
    total = peewee.DecimalField(decimal_places=2)               # 总交易额（只有人民币交易市场才会返回）
    status = peewee.SmallIntegerField()                         # 状态　0未成交　1部分成交　2已完成　3已取消 4废弃（该状态已不再使用） 5异常 6部分成交已取消 7队列中

    class Meta:
        database = db


class Digiccy(peewee.Model):
    coin_type = CoinTypeField()
    purchased_at = DateTimeField()
    price = peewee.FloatField()
    amount = peewee.FloatField()


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
Order.create_table(fail_silently=True)


if __name__ == '__main__':
    samples = [
        ["20170818001000000", 28948.27, 29027.53, 28893.54, 28912.04, 221.3961],
        ["20170818001500000", 28912.04, 28919.00, 28912.04, 28918.99, 0.4304]
    ]
    for line in samples:
        create_kline('eth', line)
    print KLine.select().count()
    line = KLine.select().order_by(KLine.started_at.desc()).first()
    print line.started_at
