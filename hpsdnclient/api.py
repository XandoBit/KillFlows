#!/usr/bin/env python
#
# ******APP externa de prueba para matar los flows ******
"""Esta biblioteca proporciona una interfaz de Python para la HP SDN
API Controller"""


from hpsdnclient.apibase import ApiBase
from hpsdnclient.core import CoreMixin
from hpsdnclient.net import NetMixin
from hpsdnclient.of import OfMixin
from hpsdnclient.rest import RestClient


class Api(CoreMixin, OfMixin, NetMixin, ApiBase):
    """ The container class for the HP SDN Controller Api """
    def __init__(self, controller, auth):
        self.restclient = RestClient(auth)
        super(Api, self).__init__(controller, self.restclient)
