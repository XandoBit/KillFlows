#!/usr/bin/env python
#
# ******APP de prueba para matar los flows ******


import os
import unittest
import hpsdnclient as hp

SDNCTL = os.getenv("SDNCTL")
USER = os.getenv("SDNUSER")
PASS = os.getenv("SDNPASS")

class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        auth = hp.XAuthToken(server=SDNCTL, user=USER, password=PASS)
        cls.api = hp.Api(controller=SDNCTL, auth=auth)

    @classmethod
    def tearDownClass(cls):
        cls.api = None

