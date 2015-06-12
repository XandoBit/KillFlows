#!/usr/bin/env python
#
# ******Tests utils******

import unittest
from hpsdnclient import utils as utils

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.mac_string = '00:00:00:00:00:01'
        self.mac_hex = '0x1'
        self.dpid_string = '00:00:00:00:00:00:00:02'
        self.dpid_hex = '0x2'

    def tearDown(self):
        pass

    def test_mac_string_to_hex(self):
        tmp = utils.string_to_hex(self.mac_string, utils.MAC)
        self.assertEqual(tmp, self.mac_hex)

    def test_dpid_string_to_hex(self):
        tmp = utils.string_to_hex(self.dpid_string, utils.DPID)
        self.assertEqual(tmp, self.dpid_hex)

    def test_mac_hex_to_string(self):
        tmp = utils.hex_to_string(self.mac_hex, utils.MAC)
        self.assertEqual(tmp, self.mac_string)

    def test_dpid_hex_to_string(self):
        tmp = utils.hex_to_string(self.dpid_hex, utils.DPID)
        self.assertEqual(tmp, self.dpid_string)


