#!/usr/bin/env python
#
# ******Fichero de Nucleo ******

import json
import time

import requests

from hpsdnclient.api import ApiBase
from hpsdnclient.error import raise_errors


class CoreMixin(ApiBase):
    """
    Esta clase contiene métodos que requieren las funciones de la API REST en Core
    Controlador HP VAN SDN

    - Gestión de aplicaciones
    - Autenticación
    - Gestión controlador
        - Registros
        - Informes de Apoyo
    - Licencias

    """
    def __init__(self, controller, auth):
        super(CoreMixin, self).__init__(controller, auth)
        self._core_base_url = ("https://{0}:8443".format(self.controller) +
                               "/sdn/v2.0/")

    def get_support(self, id=None, fields=None):
        """Genera un informe de apoyo

       : param Identificación str : Una coma separados lista de identificadores que se devuelva ( Opcional)
       : campos str param : Los campos a ser devueltos ( Opcional)
       : retorno : El informe de apoyo
       : RTYPE : hpsdnclient.datatypes.Support
         """
        url = self._core_base_url + 'support'
        if id and fields:
            url += '?id={}&fields={}'.format(id, fields)
        elif id:
            url += '?id={}'.format(id)
        elif fields:
            url += '?fields={}'.format(fields)
        return self.restclient.get(url)

    def get_licenses(self, key=None):
        """ Obtiene todas las licencias conocidas o encontrar una licencia específica por clave

       : clave str param : Una clave de licencia específica para encontrar ( Opcional)
       : return : Una lista de licencias
       : RTYPE : Lista

        """
        url = self._core_base_url + 'licenses'
        if key:
            url += '?key={}'.format(key)
        self.restclient.get(url)

    def add_license(self, key):
        """ Add a new license

       :param str key: The license key to add

        """
        url = self._core_base_url + 'licenses'
        r = self.restclient.post(url, key)
        raise_errors(r)

    def get_install_id(self):
        """ Obtiene install id

        :return: Install ID
        :rtype: str

        """
        url = self._core_base_url + 'licenses/installid'
        return self.restclient.get(url)

    def get_licence_detail(self, serial_no):
        """ Obtener unos detalles de la licencia dan su número de serie

        : param str serial_no : El número de serie para recuperar datos para
        : Detalles de la licencia : el regreso
        : RTYPE : hpsdnclient.datatypes.License

        """
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        return self.restclient.get(url)

    def deactivate_license(self, serial_no):
        """ Desactivar una licencia

        : param str serial_no : El número de serie de la licencia para deactivatee

        """
        action = json.dumps({"action": "deactivate"})
        url = self._core_base_url + 'licenses/{}'.format(serial_no)
        r = self.restclient.post(url, action)
        raise_errors(r)

    # Config data structure is wild! Need to find a way to tame it
    #
    # def get_configs(self):
    #    """ Get a list of configuration paramters """
    #    pass
    #
    # def get_config_component(self, component):
    #    #As above
    #    pass
    #
    # def update_config_component(self, component):
    #    pass
    #
    # def delete_config_component(self, component):
    #    """ Revert a configuration to default """
    #    pass

    def get_apps(self):
        """ Obtener una lista de aplicaciones de carga en el controlador

        : return : Lista de aplicaciones
        : RTYPE : Lista

        """
        url = self._core_base_url + 'apps'
        return self.restclient.get(url)

    def upload_app(self, app):
        """ Sube una aplicación para el controlador

        : app param nombre : La ruta de acceso al archivo sea cargado

        """
        url = self._core_base_url + 'apps'
        r = self.restclient.post(url, app, is_file=True)
        raise_errors(r)

    def get_app_info(self, app):
        """ Obtener información acerca de la aplicación especificada

        : app str param : La aplicación para consultar información
        : return : información de la aplicación
        : RTYPE : hpsdnclient.datatypes.App
        """
        url = self._core_base_url + 'apps/{}'.format(app)
        return self.restclient.get(url)

    def uninstall_app(self, app):
        """ Uninstall and delete an application from the controller

        :param str app: The application to be uninstalled

        """
        url = self._core_base_url + 'apps/{}'.format(app)
        r = self.restclient.delete(url)
        raise_errors(r)

    def manage_app(self, app, action):
        """ instalar , Iniciar o detener una aplicación en el controlador

        : app str param : La aplicación para gestionar
        : acción str param : La acción a realizar ( "start" , " stop " o " instalar" )

        """
        url = self._core_base_url + 'apps/{}/action'.format(app)
        r = self.restclient.post(url, action)
        raise_errors(r)

    def get_app_health(self, app):
        """ Obtener información sobre la salud de aplicación devuelto por la aplicación

        : app str param : La aplicación para consultar
        : información de salud Aplicación: retorno
        : RTYPE : hpsdnclient.datatypes.AppHealth

        """
        url = self._core_base_url + 'apps/{}/health'.format(app)
        return self.restclient.get(url)

    def download_logs(self):
        """ Descargas archivos de registro para el equipo controlador.
        Los registros son un archivo zip que contiene un archivo zip interno de registros para cada
        member.este equipo se guarda en la ruta donde la aplicación está siendo
        correr.

        : Ruta de archivo : return
        : RTYPE : String

        """
        url = self._core_base_url + 'logs'
        return self.restclient.get(url, is_file=True)

    def login(self, user, password):
        """ Entrar al controlador.
        Aunque no es necesario ( como la SDN -cliente CV maneja esto para usted )
        que está incluido aquí para completar

        : usuario str param : Nombre de usuario
        : contraseña str param : Contraseña
        : return : Diccionario que contiene simbólico y caducidad Tiempo
        : RTYPE : dict

        """
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        data = {'login': {'user': user, 'password': password}}
        r = requests.post(url, data=json.dumps(data), verify=False, timeout=1)
        t = {}
        r.raise_for_status()
        data = r.json()
        t['token'] = data[u'record'][u'token']
        exptime = data[u'record'][u'expiration']/1000
        t['token_expiration'] = time.gmtime(exptime)
        return t

    def logout(self, token):
        """ Salir del controlador
        Cierra la sesión del usuario con el token suministrado

        : símbolo str param : X -Auth - simbólico de que el usuario cierre de sesión

        """
        url = 'https://{0}:8443/sdn/v2.0/auth'.format(self.controller)
        headers = {"X-Auth-Token": token}
        r = requests.delete(url, headers=headers, verify=False, timeout=1)
        r.raise_for_status()
