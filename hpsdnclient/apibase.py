#!/usr/bin/env python
#
# ******APP externa de prueba para matar los flows ******


class ApiBase(object):
    """Clase base del objeto API"""

    def __init__(self, controller, rest_client):
        self.controller = controller
        self.rest_client = rest_client
