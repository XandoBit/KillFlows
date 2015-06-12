#!/usr/bin/env python
#
# ******Fichero de autentificación ******

import json
import datetime

import requests


class XAuthToken(requests.auth.AuthBase):
    """Esta clase se encarga de la autenticación en contra de la API REST y HP SDN
    utiliza la API de Solicitudes. XAuthToken deriva de
    requests.auth.AuthBase y hpsdnclient.ApiBase."""

    def __init__(self, server, user, password):
        """Inicializa la clase. Establecer el servidor , el usuario y variables miembro PASSW .    Establece los valores simbólicos y de vencimiento de ninguno.
"""
        super(XAuthToken, self).__init__()
        self.server = server
        self.user = user
        self.password = password
        self.token = None
        self.token_expiration = None

    def __call__(self, request):
        """TEste método se llama cuando un token de autenticación es requerido. En primer lugar, comprobar que existe el token y no tiene expirado y luego devolver el encabezado de solicitud X -Auth - Token .
"""
        if (self.token is None or
                self.token_expiration <= datetime.datetime.now()):
            self.get_auth()
        request.headers['X-Auth-Token'] = self.token
        return request

    def get_auth(self):
        """Este método solicita un token de autenticación de la SDN controlador y devuelve un diccionario con el token y tiempo de caducidad .
"""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.server)
        payload = {'login': {'user': self.user, 'password': self.password}}
        r = requests.post(url, data=json.dumps(payload),
                          verify=False, timeout=0.5)
        r.raise_for_status()
        data = r.json()
        self.token = data[u'record'][u'token']
        timestamp = data[u'record'][u'expiration'] / 1000
        self.token_expiration = datetime.datetime.fromtimestamp(timestamp)

    def delete_auth(self):
        """Eliminar de autenticación del token , AKA, Salir . Este método logs el usuario actual."""
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.server)
        headers = {"X-Auth-Token": self.token}
        r = requests.delete(url, headers=headers,
                            verify=False, timeout=0.5)
        r.raise_for_status()
        self.token = None
        self.token_expiration = None
