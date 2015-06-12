#!/usr/bin/env python
#
# ******Fichero de openflows******

import json
# Python3 compatibility
try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from hpsdnclient.api import ApiBase
import hpsdnclient.datatypes as datatypes
from hpsdnclient.error import raise_errors, DatatypeError


class OfMixin(ApiBase):
    """Métodos API REST OpenFlow

    Esta clase contiene métodos que llaman a la OpenFlow
    API REST en el controlador HP VAN SDN

    - Servicio de topología
    - Servicio de Nodo
    - Servicio de Enlace
    - Planificador de Ruta
    - Ruta Diagnóstico Servicio

    """
    def __init__(self, controller, restclient):
        super(OfMixin, self).__init__(controller, restclient)
        self._of_base_url = ("https://{0}:8443".format(self.controller) +
                             "/sdn/v2.0/of/")

    def get_stats(self):
        """Estadística de controladores Lista de todos los controladores que son
        parte del equipo de este controlador.

        : return : Lista de las estadísticas
        : RTYPE : hpsdnclient.datatypes.Stats"""
        url = self._of_base_url + 'stats'
        return self.restclient.get(url)

    def get_port_stats(self, dpid, port_id=None):
        """Enumere todas las estadísticas del puerto por un camino de datos determinada, para una
        camino de datos dado y el número de puerto

        : param str dpid : Filtrar por Datapath ID
        : param str ID_de_Puerto : Filtrar por ID de puerto
        : Vueltas: Estadísticas para Puerto
        : RTYPE : hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/ports?dpid={0}'.format(urllib.quote(dpid)))
        if port_id:
            url = url + '&port_id={0}'.format(port_id)
        return self.restclient.get(url)

    def get_group_stats(self, dpid, group_id=None):
        """Estadísticas del grupo Lista

        : param str dpid : Filtrar por Datapath ID
        : group_id param : Filtrar por ID de grupo
        : Vuelta: Estadísticas de los grupos
        : RTYPE : hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/groups?dpid={0}'.format(urllib.quote(dpid)))
        if group_id:
            url = url + '&group_id={0}'.format(group_id)
        return self.restclient.get(url)

    def get_meter_stats(self, dpid, meter_id):
        """Estadísticas metros Lista para:

        : param str dpid : El Datapath ID
        : param str meter_id : El medidor de Identificación
        : Vuelta: estadísticas Meter
        : RTYPE : hpsdnclient.datatypes.Stats

        """
        url = (self._of_base_url +
               'stats/meters?dpid={0}&meter={1}'.format(urllib.quote(dpid),
                                                        meter_id))
        return self.restclient.get(url)

    def get_datapaths(self):
        """Lista de todos los caminos de datos que son administrados por este controlador.

        : return : Una lista de datapaths
        : RTYPE : Lista

        """
        url = self._of_base_url + 'datapaths'
        return self.restclient.get(url)

    def get_datapath_detail(self, dpid):
        """Obtenga información detallada para un camino de datos .

        : param str dpid : El camino de datos de identificación
        : Vuelta: Datatpath detalles
        : RTYPE : hpsdnclient.datatypes.Datapath

        """
        url = (self._of_base_url + 'datapaths/{0}'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def get_meter_features(self, dpid):
        """Obtén características metros para el proporcionado Datapath ID

        : param str dpid : El Datapath ID
        : Vuelta: Características Meter
        : RTYPE : hpsdnclient.datatypes.MeterFeatures

        """

        url = (self._of_base_url +
               'datapaths/{0}/features/meter'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def get_group_features(self, dpid):
        """Obtén camino de datos características de grupo

        : param str dpid : El Datapath ID
        : Vuelta: Funciones del grupo
        : RTYPE : hpsdnclient.datatypes.GroupFeatures

        """
        url = (self._of_base_url +
               'datapaths/{0}/features/group'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def get_ports(self, dpid):
        """ Obtiene una lista de los puertos de la DPID especificada

        : param str dpid : El camino de datos de identificación
        : return : Lista de los puertos
        : RTYPE : Lista
        """
        url = (self._of_base_url +
               'datapaths/{0}/ports'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def get_port_detail(self, dpid, port_id):
        """ Obtiene información detallada de puerto para el puerto especificado

        : param str dpid : El camino de datos de identificación
        : param str ID_de_Puerto : El ID de puerto
        : Vuelta: detalles Portuarias
        : RTYPE : hpsdnclient.datatypes.Port

        """
        url = (self._of_base_url +
               'datapaths/{0}/ports/{1}'.format(urllib.quote(dpid), port_id))
        return self.restclient.get(url)

    def get_meters(self, dpid):
        """Lista de todos los metros configurados en el DPID suministrado

        : param str dpid : El camino de datos de identificación
        : devuelve : Una lista de los metros
        : RTYPE : Lista

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def add_meter(self, dpid, meter):
        """Añadir un nuevo medidor a la DPID suministrado

        : param str dpid :
        : param hpsdnclient.datatypes.Meter metro : El nuevo objeto Meter

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters'.format(urllib.quote(dpid)))
        r = self.restclient.post(url, json.dumps(meter.to_dict()))
        raise_errors(r)

    def get_meter_details(self, dpid, meter_id):
        """Información detallada metros

        : param str dpid : El camino de datos de identificación
        : param str meter_id : El ID de metro
        : Vuelta: detalles Meter
        : RTYPE : hpsdnclient.datatypes.Meter

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        return self.restclient.get(url)

    def update_meter(self, dpid, meter_id, meter):
        """ Actualizar el metro especificado

        : param str dpid : El camino de datos de identificación
        : param str meter_id : El ID de metro
        : param hpsdnclient.datatypes.Meter metro : El metro

        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        r = self.restclient.put(url, meter)
        raise_errors(r)

    def delete_meter(self, dpid, meter_id):
        """Eliminar un metro

        : param str dpid : El camino de datos de identificación
        : param str meter_id : El ID de metro a borrar
        """
        url = (self._of_base_url +
               'datapaths/{0}/meters/{1}'.format(urllib.quote(dpid), meter_id))
        r = self.restclient.put(url, self.auth)
        raise_errors(r)

    def get_flows(self, dpid):
        """Obtiene una lista de los flujos en el DPID suministrado


        : param str dpid : El camino de datos de identificación
        : return : Lista de los flujos
        : RTYPE : Lista
        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        return self.restclient.get(url)

    def _assemble_flows(self, flows):
        if isinstance(flows, list):
            tmp = []
            for f in flows:
                if isinstance(f, datatypes.Flow):
                    tmp.append(f.to_dict())
                else:
                    raise DatatypeError(datatypes.Flow, f.__class__())
            data = {"flows": tmp}
        elif isinstance(flows, datatypes.Flow):
            data = {"flow": flows.to_dict()}
        else:
            raise DatatypeError([datatypes.Flow, list], f.__class__())
        return data

    def add_flows(self, dpid, flows):
        """Añadir un flujo o flujos a la DPID seleccionado

        : param str dpid : El camino de datos de identificación
        : Lista param , hpsdnclient.datatypes.Flow fluye : El flujo o flujos de añadir

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def update_flows(self, dpid, flows):
        """Actualización de un flujo o flujos en el DPID seleccionado

        : param str dpid : El camino de datos de identificación
        : Lista param , hpsdnclient.datatypes.Flow fluye :
            El flujo o flujos para actualizar
        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.put(url, json.dumps(data))
        raise_errors(r)

    def delete_flows(self, dpid, flows):
        """ Eliminar flujo , o en los flujos de la DPID especificada

        : param str dpid : El camino de datos de identificación
        : Lista param , hpsdnclient.datatypes.Flow fluye :
            El flujo o los flujos de suprimir

        """
        url = (self._of_base_url +
               'datapaths/{0}/flows'.format(urllib.quote(dpid)))
        data = self._assemble_flows(flows)
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

    def get_groups(self, dpid):
        """Obtener una lista de los grupos creados en el DPID

        : param str dpid : El camino de datos de identificación
        : return : Lista de grupos
        : RTYPE : Lista
        """
        url = (self._of_base_url +
               'datapaths/{0}/groups'.format(urllib.quote(dpid)))

        return self.restclient.get(url)

    def add_group(self, dpid, group):
        """Create a group

        :param str dpid: The datapath ID
        :param hpsdnclient.datatypes.Group group: The group to add

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups'.format(urllib.quote(dpid)))
        data = {"group": group.to_dict()}
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def get_group_details(self, dpid, group_id):
        """Obtener detalles del grupo

        : param str dpid : El camino de datos de identificación
        : param str group_id : El ID de grupo
        : Vuelta: Detalles del grupo
        : RTYPE : hpsdnclient.datatypes.Group

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        return self.restclient.get(url)

    def update_group(self, dpid, group_id, group):
        """Actualización de un grupo

        : param str dpid : El camino de datos de identificación
        : Grupo hpsdnclient.datatypes.Group param : El grupo para agregar

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        r = self.restclient.post(url, json.dumps(group.to_dict()))
        raise_errors(r)

    def delete_groups(self, dpid, group_id):
        """Delete a group

        :param str dpid: The datapath ID
        :param str group_id: The group ID to delete

        """
        url = (self._of_base_url +
               'datapaths/{0}/groups/{1}'.format(urllib.quote(dpid), group_id))
        r = self.restclient.delete(url, self.auth)
        raise_errors(r)
