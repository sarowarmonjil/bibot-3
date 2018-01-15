# coding: utf-8
# http://docs.peewee-orm.com/en/latest/
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

import settings
import apis     # 这里耦合apis中定义的一些常亮


db = SqliteExtDatabase(settings.DATABASE['NAME'])


SYMBOLS = [
    (apis.BTC, apis.BTC),
]


DateTimeField = peewee.IntegerField


class SymbolField(peewee.CharField):
    def __init__(self, *args, **kws):
        kws['choices'] = SYMBOLS
        return super(SymbolField, self).__init__(*args, **kws)


class KLine(peewee.Model):
    symbol = SymbolField()
    period = peewee.CharField()
    started_at = DateTimeField()

    open = peewee.FloatField()
    high = peewee.FloatField()
    low = peewee.FloatField()
    close = peewee.FloatField()
    vol = peewee.FloatField()   # 成交额

    class Meta:
        database = db
        indexes = [
            (('symbol', 'period', 'started_at'), True),
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
    def get_latest_time(symbol=apis.BTC, period=apis._1MIN):
        line = KLine.filter(symbol=symbol, period=period).order_by(KLine.started_at.desc()).first()
        return line and line.started_at


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
    coin_type = SymbolField()
    purchased_at = DateTimeField()
    price = peewee.FloatField()
    amount = peewee.FloatField()


def create_kline(symbol, period, line):
    KLine.create(symbol=symbol,
                 period=period,
                 started_at=line['id'],
                 open=line['open'],
                 high=line['high'],
                 low=line['low'],
                 close=line['close'],
                 vol=line['vol'])


db.connect()
# https://github.com/coleifer/peewee/issues/211
KLine.create_table(fail_silently=True)
