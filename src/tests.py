# coding: utf-8
import unittest

import utils


class TestUtils(unittest.TestCase):

    def test_to_timestamp(self):
        datetime, timestamp = ('20170818220900000', 1503065340.0)
        self.assertEqual(utils.to_timestamp(datetime), timestamp)

    def test_sign(self):
        signature = utils.sign({'a': 1})
        self.assertEqual(signature, '3872c9ae3f427af0be0ead09d07ae2cf')

    def test_to_decimal(self):
        samples = [
            (2, '2.00'),
            (2.1, '2.10'),
            (2.114, '2.11'),
            (2.115, '2.12'),
            ('2.11', '2.11'),
        ]
        for p, d in samples:
            self.assertEqual(utils.to_decimal(p, 2), d)
