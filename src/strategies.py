# coding: utf-8
import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, report, training, utils, Variable
from chainer import datasets, iterators, optimizers, serializers
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions
from chainer.variable import Parameter
import random


class Linear(object):

    def __init__(self, in_dim, out_dim):
        self.W = np.mat(np.random.random((in_dim, out_dim)))
        self.b = np.mat(np.random.random((1, out_dim)))


class Policy(Chain):
    out_dim = 3

    def __init__(self):
        super(Policy, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(84)
            self.l2 = L.Linear(self.out_dim, nobias=True)

    def forward(self, x):
        if not isinstance(x, chainer.Variable):
            if not isinstance(x, np.ndarray) or x.dtype != np.float32:
                x = np.array(x, dtype=np.float32)
            x = chainer.Variable(x)
        z = F.relu(self.l1(x))
        z = self.l2(z)
        result = F.argmax(z, 1).data
        return result

    @staticmethod
    def variation_1(a):
        a += a * np.random.binomial(2, 0.1, a.shape) * np.random.normal(size=a.shape)
        return a

    @staticmethod
    def variation_3(a):
        return a

    @staticmethod
    def _breed_1(v1, v2):
        t = np.random.binomial(2, 0.7, v1.shape)
        return (v1 * t + v2 * (1 - t)).astype(np.float32)

    @staticmethod
    def _breed_2(v1, v2):
        v = v1 if random.random() < 0.0 else v2
        return v.copy()

    @staticmethod
    def _breed_3(v1, v2):
        return v1.copy()

    @staticmethod
    def breed(p1, p2):
        p = Policy()
        W = Policy._breed_2(p1.l1.W.data, p2.l1.W.data)   # NOQA
        b = Policy._breed_2(p1.l1.b.data, p2.l1.b.data)
        p.l1.W = Parameter(W)
        p.l1.b = Parameter(b)

        W = Policy._breed_2(p1.l2.W.data, p2.l2.W.data)   # NOQA
        p.l2.W = Parameter(W)

        return p

    def variation(self):
        self.variation_1(self.l1.W.data)
        self.variation_1(self.l1.b.data)
        self.variation_1(self.l2.W.data)

    def __call__(self, x):
        return self.forward(x)

    def dump(self, name='my.model'):
        serializers.save_npz(name, self)

    def load(self, name='my.model'):
        serializers.load_npz(name, self)

if __name__ == '__main__':
    p = Policy()
    print p([[1, 2, 3]]).data
