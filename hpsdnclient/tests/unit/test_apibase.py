#!/usr/bin/env python
#
# ******Tests api base ******

import unittest

from hpsdnclient.apibase import ApiBase
from hpsdnclient.rest import RestClient
from hpsdnclient.auth import XAuthToken


class ApiBaseTest(unittest.TestCase):
    def test_apibase_instantiation(self):
        controller = '127.0.0.1'
        token = XAuthToken('127.0.0.1', 'sdn', 'skyline')
        rest_client = RestClient(token)
        apibase = ApiBase(controller, rest_client)
        self.assertEqual(apibase.controller, controller)
        self.assertEqual(apibase.rest_client, rest_client)
