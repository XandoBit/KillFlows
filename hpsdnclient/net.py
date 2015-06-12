#!/usr/bin/env python
#
# ******Fichero de net******

import json
import urllib

from hpsdnclient.api import ApiBase
from hpsdnclient.error import raise_errors
from hpsdnclient.datatypes import LldpProperties


class NetMixin(ApiBase):
    """Métodos API Red de Servicios REST

    Esta clase contiene métodos que requieren los servicios de red
    Funciones de la API REST en el controlador HP VAN SDN

    - Servicio de topología
    - Servicio de Nodo
    - Servicio de Enlace
    - Planificador de Ruta
    - Ruta Diagnóstico Servicio

    """
    def __init__(self, controller, auth):
        super(NetMixin, self).__init__(controller, auth)
        self._net_base_url = ("https://{0}:8443".format(self.controller) +
                              "/sdn/v2.0/net/")
        self._diag_base_url = ("https://{0}:8443".format(self.controller) +
                               "/sdn/v2.0/diag/")

    def get_clusters(self):
        """ Obtiene una lista de los clusters

        : return : Una lista de los clusters
        : RTYPE : Lista

        """
        url = self._net_base_url + 'clusters'
        return self.restclient.get(url)

    def get_cluster_broadcast_tree(self, cluster_id):
        """ Obtiene el árbol de transmisión para un grupo específico

        : param str CLUSTER_ID : El ID de clúster
        : retorno : El árbol de transmisión para la ID de clúster proporcionado
        : RTYPE : hpsdnclient.datatypes.Cluster

        """
        url = self._net_base_url + 'clusters/{0}/tree'.format(cluster_id)
        return self.restclient.get(url)

    def get_links(self, dpid=None):
        """ Devuelve una lista de todos los enlaces descubiertos por el controlador SDN

        : param str dpid : Devolver sólo los enlaces para la DPID especificada
        : return : Una lista de Enlaces
        : RTYPE : Lista

        """
        url = self._net_base_url + 'links'
        if dpid:
            url = url + '?dpid={0}'.format(urllib.quote(dpid))
        return self.restclient.get(url)

    def get_forward_path(self, src_dpid, dst_dpid):
        """ Obtiene el camino más corto entre computarizada src_dpid y dst_dpid

        : param str src_dpid : La fuente DPID
        : param str dst_dpid : El destino DPID
        : retorno : El camino más corto entre los dos DPID de
        : RTYPE : hpsdnclient.datatypes.Path
        """
        url = (self._net_base_url +
               'paths/forward' +
               '?src_dpid={0}&dst_dpid={1}'.format(urllib.quote(src_dpid),
                                                   urllib.quote(dst_dpid)))
        return self.restclient.get(url)

    def get_arps(self, vid=None, ip=None):
        """ Proporciona detalles ARP para la dirección IP dada y VLAN ID

        : param str vid : Volver ARP en el proporcionado VLAN ID
        : param str ip : Regresa sólo el ARP para la dirección IP especificada
        : return : Lista de ARP
        : RTYPE : Lista

        """
        url = self._net_base_url + 'arps'

        if vid and not ip:
            url = url + "?vid={0}".format(vid, ip)
        elif vid and ip:
            url = url + "?vid={0}&ip={1}".format(vid, ip)

        return self.restclient.get(url)

    def get_nodes(self, ip=None, vid=None, dpid=None, port=None):
        """ Obtener todos los nodos descubiertos por el controlador

        - Con ` ip`` y` ` vid`` vuelve detalles nodo
        - Con `` vid`` vuelve nodos en la VLAN especificada
        - Con `` dpid`` vuelve nodos conectados a la DPID especificada
        - Con '' y `` dpid`` port`` vuelve Nodos para determinado puerto / DPID

        : str param ip : Dirección IP
        : str param vid : VLAN ID
        : param str dpid : Datapath ID
        : puerto str param : Port

        """
        url = self._net_base_url + 'nodes'

        if vid and not ip:
            url += "?vid={0}".format(vid, ip)
        elif vid and ip:
            url += "?vid={0}&ip={1}".format(vid, ip)
        elif dpid and not port:
            url += "?dpid={0}".format(urllib.quote(dpid))
        elif dpid and port:
            url += "?dpid={0}&port={1}".format(urllib.quote(dpid), port)

        return self.restclient.get(url)

    def get_lldp_suppressed_ports(self):
        """ Obtiene una lista de puertos LLDP suprimidos desde el controlador

        : return : Una lista de puertos en el estado LLDP suprimido
        : RTYPE : Lista
        """
        url = self._net_base_url + 'lldp'
        return self.restclient.get(url)

    def set_lldp_suppressed(self, ports):
        """ Pone los puertos previstos para LLDP suprimido estado

        : params puertos str : Los puertos que se suprimen

        """
        if isinstance(ports, list):
            tmp = []
            for item in list:
                if isinstance(item, LldpProperties):
                    tmp.append(item.to_dict())
                else:
                    tmp.append(item)
            data = {"lldp_suppressed": tmp}

        else:
            data = {"lldp_suppressed": [ports.to_dict()]}

        url = self._net_base_url + 'lldp'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def remove_lldp_suppressed(self, ports):
        """ Elimina los puertos de LLDP suprimido estado

        : params puertos hpsdnclient.datatypes.LldpProperties :
            Los puertos para ser removidos de LLDP suprimido estado

        """

        if isinstance(ports, list):
            tmp = []
            for item in list:
                if isinstance(item, LldpProperties):
                    tmp.append(item.to_dict())
                else:
                    tmp.append(item)
            data = {"lldp_suppressed": tmp}

        else:
            data = {"lldp_suppressed": [ports.to_dict()]}
        url = self._net_base_url + 'lldp'
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

    def get_diag_observation_posts(self, packet_uid=None, packet_type=None):
        """ Obtiene una lista de los puestos de observación de diagnóstico

        : param str packet_uid : devolver sólo OP de la UID de paquetes proporcionado
        : param str packet_type : Regresa sólo OP de con el tipo de paquete proporcionado
        : return : Lista de OP de
        : RTYPE : Lista

        """
        url = self._diag_base_url + 'observations'
        if packet_uid:
            url += '?packet_uid={}'.format(packet_uid)
        if packet_type:
            url += '?packet_type={}'.format(packet_type)
        return self.restclient.get(url)

    def create_diag_observation_post(self, observation):
        """ Crea un puesto de observación de diagnóstico

        : hpsdnclient.datatypes.Observation param observación:
            El puesto de observación para crear

        """
        data = {"observation": observation.to_dict()}
        url = self._diag_base_url + 'observations'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def delete_diag_observation_post(self, observation):
        """ Eliminar un puesto de observación de diagnóstico

        : str param observación: El puesto de observación para borrar

        """
        data = {"observation": observation.to_dict()}
        url = self._diag_base_url + 'observations'
        r = self.restclient.delete(url, json.dumps(data))
        raise_errors(r)

    def get_diag_packets(self, packet_type=None):
        """ Obtenga una lista de todos los paquetes de diagnóstico en el sistema

        : resultado Filtrar por siempre el tipo de paquete : packet_type param
        : return : Una lista de los paquetes de diagnóstico
        : RTYPE : Lista

        """
        url = self._diag_base_url + 'packets'
        if packet_type:
            url += '?type{}'.format(packet_type)
        return self.restclient.get(url)

    def create_diag_packet(self, packet):
        """ Ccrear un paquete de diagnóstico

        : paquete str param : El paquete para crear

        """
        data = {"packet": packet.to_dict()}
        url = self._diag_base_url + 'packets'
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)

    def delete_diag_packet(self, packet_uid):
        """ Eliminar un paquete de diagnóstico

        : param str packet_uid : El fluido del paquete que desea eliminar



        """
        url = self._diag_base_url + 'packets/{}'.format(packet_uid)
        r = self.restclient.delete(url)
        raise_errors(r)

    def get_diag_packet(self, packet_uid):
        """ Obtener datos de diagnóstico de paquetes para el paquete UID proporcionado

        : param str packet_uid : El UID de paquetes para obtener detalles
        : Vuelta: Diagnóstico de paquetes Detalles
        : RTYPE : hpsdnclient.datatypes.Packet
        """
        url = self._diag_base_url + 'packets/{}'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_path(self, packet_uid):
        """ Obtén caminos previstos para paquete de diagnóstico

        : param packet_uid : El UID del paquete de diagnóstico
        : return : Camino
        : RTYPE : hpsdnclient.datatypes.Path

        """
        url = self._diag_base_url + 'packets/{}/path'.format(packet_uid)
        return self.restclient.get(url)

    def get_diag_packet_nexthop(self, packet_uid, dpid):
        """ Mostrar información siguiente salto para paquetes en un determinado Datapath ID

        : param str packet_uid : El UID de paquetes
        : param str dpid : El Datapath ID
        : devuelve : El siguiente salto
        : RTYPE : hpsdnclient.datatypes.NextHop

        """
        url = self._diag_base_url + 'packets/{}/nexthops'.format(packet_uid)
        url += '?src_dpid={}'.format(dpid)
        return self.restclient.get(url)

    def set_diag_packet_action(self, packet_uid, action):
        """ Realiza la acción de simulación especificado en un paquete

        : param str packet_uid : El UID de paquetes
        : acción str param : La acción a realizar
        """
        data = {"simulation": action}
        url = self._diag_base_url + 'packets/{}/action'.format(packet_uid)
        r = self.restclient.post(url, json.dumps(data))
        raise_errors(r)
