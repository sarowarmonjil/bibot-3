# coding: utf-8
'''
给出每分钟的技术分析
'''
import numpy as np
import talib

import utils


def _normal(array, scale, offset, min_value, max_value):
    array *= scale
    array += offset
    array[array < min_value] = min_value
    array[array > max_value] = max_value
    return array


def gen_raw_features(close, *args):
    # 确保参数顺序
    args = list(args)
    args.sort()
    close = np.asarray(close, dtype=np.float64)     # talib 要求输入数组为双精度浮点数
    # 装填特征
    features = []
    # PPO
    for fast_period, slow_period in utils.pairwise(args):
        f = talib.PPO(close, fast_period, slow_period, 1) / 100     # 最后的 1 表示使用指数移动平均
        features.append(f)
    # ROCP
    for period in args:
        f = talib.ROCP(close, period) / period
        features.append(f)
    # 拼接
    features = [f.reshape(-1, 1) for f in features]
    features = np.concatenate(features, axis=1)
    # 去除无效点
    return features[args[-1]:]


def gen_human_features(close, *args):
    features = gen_raw_features(close, *args)
    _normal(features[:len(args) - 1], 1000, 10, 0, 20)
    _normal(features[len(args) - 1:], 50000, 10, 0, 20)
    return features


def onehot(features, max_value=20):
    line = features.shape[0]
    nb_classes = max_value + 1
    features = features.astype(np.int32)
    features = features.reshape(-1)
    # Chainer 需要float32的数据，这里耦合一下。
    features = np.eye(nb_classes, dtype=np.float32)[features]
    return features.reshape(line, -1)


def gen_machine_features(close, *args):
    features = gen_human_features(close, *args)
    return onehot(features)


def _features(close):
    return gen_machine_features(close, 30, 400)


def describe(features):
    print features.mean(axis=0)
    print features.min(axis=0)
    print features.max(axis=0)
    print features.std(axis=0)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import orm

    qs = orm.KLine.select(orm.KLine.closing).filter(coin_type='btc', period=1)
    qs = qs.order_by(orm.KLine.started_at)
    close = [line.closing for line in qs]

    features = gen_raw_features(close, 2, 30, 400)
    describe(features)

    data = gen_human_features(close, 2, 30, 400)
    describe(data)

    print data.shape, data.dtype
    # plt.plot(data[:, 1:])
    for idx, color in [(0, 'b'), (1, 'g'), (2, 'r'), (3, 'c'), (4, 'y')]:
        plt.plot(data[:, idx:idx + 1], color)
    plt.show()
