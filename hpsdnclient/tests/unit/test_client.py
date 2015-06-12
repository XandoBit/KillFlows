#!/usr/bin/env python
#
# ******Tests clientes ******

import unittest

from hpsdnclient.api import Api
from hpsdnclient.auth import XAuthToken
from hpsdnclient.apibase import ApiBase
from hpsdnclient.core import CoreMixin
from hpsdnclient.net import NetMixin
from hpsdnclient.of import OfMixin


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.auth = XAuthToken(server='example.com',
                               user='sdn',
                               password='skyline'
        )

    def test_api_instantiation(self):
        api = Api('10.10.10.10', self.auth)
        self.assertTrue(isinstance(api, ApiBase))
        self.assertTrue(isinstance(api, CoreMixin))
        self.assertTrue(isinstance(api, NetMixin))
        self.assertTrue(isinstance(api, OfMixin))
        self.assertEqual(api.restclient.auth, self.auth)
        self.assertEqual(api.controller, '10.10.10.10')
