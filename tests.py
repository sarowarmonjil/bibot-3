# coding: utf-8
import unittest

import utils


class TestUtils(unittest.TestCase):

    def test_to_timestamp(self):
        datetime, timestamp = ('20170818220900000', 1503065340.0)
        self.assertEqual(utils.to_timestamp(datetime), timestamp)
