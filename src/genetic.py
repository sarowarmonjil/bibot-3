# coding: utf-8
# 个体——单维度numpy数组
# 直接保留的个体比例
# 淘汰率
import numpy as np

from ta import _get_test_data
from strategies import Policy
import utils


def breed(a, b):
    return (a + b) / 2


def variation(a):
    a += np.random.binomial(2, 0.1, a.shape) * np.random.normal(a.shape)
    return a


def score(a):
    return np.abs(a - 5)


def normal(array):
    array = np.array(array, dtype=np.float32)
    print array
    print array.min(), array.max(), np.average(array)

    array -= array.min() - 0.002
    # array += array.max()
    # array += 10
    return array / np.sum(array)


class Population(object):
    def __init__(self, n):
        self.n = n
        self.peoples = [Policy() for _ in xrange(n)]
        # self.peoples[0].load()
        self.close, self.values = _get_test_data()

    def grab_best(self, n):
        idx_list = self.scores.argsort()
        return [self.peoples[idx] for idx in idx_list[-n:]]

    def sim(self):
        print 'peoples:', len(self.peoples)
        scores = []
        for idx, p in enumerate(self.peoples):
            d = p(self.values)
            score = utils.evaluate(zip(d, self.close))
            scores.append(score)
        p = normal(scores)
        idx_list = p.argsort()
        peoples = []
        for idx in idx_list[-25:]:
            peoples.append(self.peoples[idx])
        self.master = self.peoples[idx_list[-1]]
        for _ in xrange(self.n - 25):
            f, m = np.random.choice(np.arange(self.n), 2, replace=False, p=p)
            t = Policy.breed(self.peoples[f], self.peoples[m])
            t.variation()
            peoples.append(t)
        self.peoples = peoples

if __name__ == '__main__':
    # p = normal(np.random.random(3))
    # print p
    # print np.random.choice(np.arange(3), 2, replace=False, p=p)
    # print variation(np.arange(10).astype(np.float32))
    p = Population(500)
    for idx in xrange(1001):
        print '---', idx, '---'
        p.sim()
        print '=== ==='

        if idx % 40 == 0:
            import matplotlib.pyplot as plt

            fig, ax1 = plt.subplots()
            ax1.plot(p.close, 'b-')
            ax1.set_xlabel('time (s)')
            # Make the y-axis label, ticks and tick labels match the line color.
            ax1.set_ylabel('price', color='b')
            ax1.tick_params('p', colors='b')

            d = p.master(p.values)

            last = 0
            data = []
            for c in d:
                if c == 2:
                    c = last
                data.append(c)
                last = c

            ax2 = ax1.twinx()
            ax2.plot(d, 'r-')
            ax2.set_ylabel('vol', color='r')
            ax2.tick_params('v', color='r')

            fig.tight_layout()
            plt.show()

            p.master.dump()
