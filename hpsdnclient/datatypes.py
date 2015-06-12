#!/usr/bin/env python
#
# ******Fichero de tipos de caracteristicas******

""" Tipos Python datos utilizados para los objetos REST"""

import json

ETHERNET = ['ipv4', 'arp', 'rarp', 'snmp', 'ipv6',
            'mpls_u', 'mpls_m', 'lldp', 'pbb', 'bddp']

VERSION = ['1.0.0', '1.1.0', '1.2.0', '1.3.0)']

ACTIONS = ['output',
           'set_vlan_vid',
           'set_vlan_pcp',
           'strip_vlan',
           'set_dl_src',
           'set_dl_dst',
           'set_nw_src',
           'set_nw_dst',
           'set_nw_tos',
           'set_tp_src',
           'set_tp_dst',
           'enqueue']

CAPABILITIES = ['flow_stats',
                'table_stats',
                'port_stats',
                'stp',
                'group_stats',
                'reserved',
                'ip_reasm',
                'queue_stats',
                'arp_match_ip',
                'port_blocked'
                ]

PORT_CONFIG = ["port_down",
               "no_stp",
               "no_recv",
               "ro_recv_stp",
               "no_flood",
               "no_fwd",
               "no_packet_in"
               ]

PORT_STATE = ["link_down",
              "blocked",
              "live",
              "stp_listen",
              "stp_learn",
              "stp_forward",
              "stp_block"
              ]

PORT_FEATURES = ["rate_10mb_hd",
                 "rate_10mb_fd",
                 "rate_100mb_hd",
                 "rate_100mb_fd",
                 "rate_1gb_hd",
                 "rate_1gb_fd",
                 "rate_10gb_fd",
                 "rate_40gb_fd",
                 "rate_100gb_fd",
                 "rate_1tb_fd",
                 "rate_other",
                 "copper",
                 "fiber",
                 "autoneg",
                 "pause",
                 "pause_asym"
                 ]

FLOW_MOD_CMD = ["add",
                "modify",
                "modify_strict",
                "delete",
                "delete_strict"
                ]

FLOW_MOD_FLAGS = ["send_flow_rem",
                  "check_overlap",
                  "emerg",
                  "reset_counts",
                  "no_packet_counts",
                  "no_byte_counts"]

IP_PROTOCOL = ["tcp",
               "udp",
               "sctp",
               "icmp",
               "ipv6-icmp"
               ]

ICMP_V6_TYPE = ["nbr_sol", "nbr_adv"]

MATCH_MODE = ["none", "present", "exact"]

IPV6_EXTHDR = ["no_next",
               "esp",
               "auth",
               "dest",
               "frag",
               "router",
               "hop",
               "un_rep",
               "un_seq"]

METER_FLAGS = ["kbps",
               "pktps",
               "burst",
               "stats"]

METER_TYPE = ["drop", "dscp_remark", "experimenter"]

GROUP_TYPE = ["all", "select", "indirect", "ff"]

COMMANDS = ["add", "modify", "delete"]

LINK_STATE = ["link_down",
              "blocked",
              "live",
              "stp_listen",
              "stp_learn",
              "stp_forward",
              "stp_block"
              ]

OPERATION = ["ADD", "CHANGE", "DELETE", "MOVE"]

ENUMS = [ETHERNET,
         VERSION,
         ACTIONS,
         CAPABILITIES,
         PORT_CONFIG,
         PORT_STATE,
         PORT_FEATURES,
         FLOW_MOD_CMD,
         FLOW_MOD_FLAGS,
         IP_PROTOCOL,
         ICMP_V6_TYPE,
         MATCH_MODE,
         ICMP_V6_TYPE,
         MATCH_MODE,
         IPV6_EXTHDR,
         METER_FLAGS,
         METER_TYPE,
         GROUP_TYPE,
         COMMANDS,
         LINK_STATE,
         OPERATION
         ]

METHODS = ["factory", "to_json_string", "to_dict"]
KEYWORDS = ["self"]

JSON_MAP = {'datapath': 'Datapath',
            'meter_features': 'MeterFeatures',
            'group_features': 'GroupFeatures',
            'port': 'Port',
            'meter': 'Meter',
            'flow': 'Flow',
            'group': 'Group',
            'cluster': 'Cluster',
            'packet': 'Packet',
            'path': 'Path',
            'app': 'App',
            'license': 'License',
            'support_report': None,
            'observation': 'Observation',
            'nexthop': 'NextHop'
            }

PLURALS = {'datapaths': JSON_MAP['datapath'],
           'controller_stats': 'ControllerStats',
           'stats': 'Stats',
           'ports': JSON_MAP['port'],
           'meters': JSON_MAP['meter'],
           'flows': JSON_MAP['flow'],
           'groups': JSON_MAP['group'],
           'clusters': JSON_MAP['cluster'],
           'links': 'Link',
           'nodes': 'Node',
           'arps': 'Arp',
           'lldp_suppressed': 'LldpProperties',
           'observations': JSON_MAP['observation'],
           'packets': JSON_MAP['packet'],
           'apps': JSON_MAP['app'],
           'licenses': JSON_MAP['license'],
           'paths': JSON_MAP['path'],
           'nexthops': JSON_MAP['nexthop']
           }

CLASS_MAP = {'ControllerStats': {'lost': 'Counter',
                                 'packet_in': 'Counter',
                                 'packet_out': 'Counter'},
             'Team': {'systems': 'TeamSystem'},
             'Flow': {'match': 'Match',
                      'actions': 'Action',
                      'instructions': 'Instruction'},
             'Stats': {'port_stats': 'PortStats',
                       'group_stats': 'GroupStats',
                       'meter_stats': 'MeterStats'},
             'Packet': {'eth': 'Ethernet',
                        'ip': 'Ip',
                        'ipv6': 'Ipv6',
                        'udp': 'Udp',
                        'tcp': 'Tcp',
                        'dhcp': 'Dhcp',
                        'icmp': 'Icmp',
                        'icmpv6': 'Icmpv6'}
             }


class JsonObjectFactory(object):

    factories = {}

    @staticmethod
    def add_factory(id, factory):
        JsonObjectFactory.factories[id] = factory

    @staticmethod
    def create(id, data):
        for key in data:
            if key in KEYWORDS:
                new_key = key + "_"
                data[new_key] = data.pop(key)
        if id not in JsonObjectFactory.factories:
            JsonObjectFactory.add_factory(id, eval(id))
        return JsonObjectFactory.factories[id].factory(data)


class JsonObject(object):

    """ Esta es la clase base para todos los tipos de datos de cliente HP SDN ."""

    def __str__(self):
        return self.to_json_string()

    def to_json_string(self):
        tmp = self.to_dict()
        return json.dumps(tmp, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def to_dict(self):
        data = {}
        attributes = [attr for attr in dir(self)
                      if not callable(getattr(self, attr)) and
                      not attr.startswith("__")]
        for attr in attributes:
            if getattr(self, attr) is not None:
                value = getattr(self, attr)
                if isinstance(value, list):
                    tmp = []
                    for list_item in value:
                        if isinstance(list_item, JsonObject):
                            tmp.append(list_item.to_dict())
                        else:
                            tmp.append(list_item)
                    data[attr.__str__()] = tmp
                elif isinstance(value, JsonObject):
                    data[attr.__str__()] = value.to_dict()
                elif type(value):
                    data[attr.__str__()] = value
        return data

    @classmethod
    def factory(cls, data):
        try:
            cm = CLASS_MAP[cls.__name__]
            for key in data:
                if key in cm and isinstance(data[key], list):
                    l = []
                    for d in data[key]:
                        l.append(JsonObjectFactory.create(cm[key], d))
                    data[key] = l
                elif key in cm:
                    data[key] = JsonObjectFactory.create(cm[key], data[key])
        except KeyError:
            pass

        return cls(**data)

    def __eq__(self, other):
        attributes = [attr for attr in dir(self)
                      if not callable(getattr(self, attr)) and
                      not attr.startswith("__")]
        for attr in attributes:
            try:
                if self.__getattribute__(attr) == other.__getattribute__(attr):
                    continue
                else:
                    return False
            except AttributeError:
                return False
        else:
            return True

# OpenFlow #


class Datapath(JsonObject):
    """ Datapath (JsonObject)

       Una representación de python del objeto Datapath.

    """
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.negotiated_version = kwargs.get('negotiated_version', None)
        self.ready = kwargs.get('ready', None)
        self.last_message = kwargs.get('last_message', None)
        self.num_buffers = kwargs.get('num_buffers', None)
        self.num_tables = kwargs.get('num_tables', None)
        self.capabilities = kwargs.get('capabilities', [])
        self.device_ip = kwargs.get('device_ip', None)
        self.device_port = kwargs.get('device_port', None)


class DatapathControllers(JsonObject):
    """Un controlador , desde un punto de vista camino de datos"""
    def __init__(self, **kwargs):
        self.master = kwargs.get('master', None)
        self.slaves = kwargs.get('slaves', [])


class MeterFeatures(JsonObject):
    def __init__(self, **kwargs):
        self.flags = kwargs.get("flags", None)
        self.max_bands_per_meter = kwargs.get("max_bands_per_meter", None)
        self.max_color_value = kwargs.get("max_color_value", None)
        self.max_meters = kwargs.get("max_meters", None)
        self.types = kwargs.get("types", None)


class GroupFeatures(JsonObject):
    """ Docstirg aqui se hace"""
    def __init__(self, **kwargs):
        self.actions = kwargs.get("actions", None)
        self.capabilities = kwargs.get("capabilities", None)
        self.max_groups = kwargs.get("max_groups", None)
        self.types = kwargs.get("types", None)


class Port(JsonObject):
    """ Port (JsonObject)

       Una representación pitón del objeto Puerto

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.mac = kwargs.get('mac', None)
        self.current_speed = kwargs.get('current_speed', None)
        self.max_speed = kwargs.get('max_speed', None)
        self.config = kwargs.get('config', [])
        self.state = kwargs.get('state', [])
        self.current_features = kwargs.get('current_features', [])
        self.advertised_features = kwargs.get('advertised_features', [])
        self.supported_features = kwargs.get('supported_features', [])
        self.peer_features = kwargs.get('peer_features', [])


class Flow(JsonObject):
    """ Flow (JsonObject)

       Una representación pitón del objeto de flujo

    """
    def __init__(self, **kwargs):
        self.table_id = kwargs.get('table_id', None)
        self.priority = kwargs.get('priority', None)
        self.match = kwargs.get('match', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.idle_timeout = kwargs.get('idle_timeout', None)
        self.hard_timeout = kwargs.get('hard_timeout', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.cookie = kwargs.get('cookie', None)
        self.cookie_mask = kwargs.get('cookie_mask', None)
        self.buffer_id = kwargs.get('buffer_id', None)
        self.out_port = kwargs.get('out_port', None)
        self.flow_mod_cmd = kwargs.get('flow_mod_cmd', None)
        self.flow_mod_flags = kwargs.get('flow_mod_flags', [])
        self.instructions = kwargs.get('instructions', [])
        self.actions = kwargs.get('actions', [])

    @classmethod
    def factory(cls, data):
        """ Override factory in the base class to create a single instance of
        the Match class for the 'match' key. We do this as each match field
        may only exist once. Actions are trickier as keys here are not unique.
        When multiple values are present, """
        try:
            cm = CLASS_MAP[cls.__name__]
            for key in data:
                if key == 'match':
                    new_match = {}
                    for d in data[key]:
                        for k in d:
                            new_match[k] = d[k]
                    data[key] = JsonObjectFactory.create('Match', new_match)
                elif key == 'actions':
                    new_action = {}
                    keys = []
                    for d in data[key]:
                        keys.extend([(k, v) for k, v in d.items()])
                    num_keys = range(len(keys))

                    duplicates = {}

                    for i in num_keys:
                        key_name = keys[i][0]
                        if key_name in duplicates:
                            duplicates[key_name].append(i)
                        else:
                            duplicates[key_name] = [i]

                    for k, v in duplicates.items():
                        if len(v) > 1:
                            new_action[k] = [keys[i][1] for i in v]
                        else:
                            new_action[k] = keys[i][1]

                    data[key] = JsonObjectFactory.create('Action', new_action)
                elif key in cm and isinstance(data[key], list):
                    l = []
                    for d in data[key]:
                        l.append(JsonObjectFactory.create(cm[key], d))
                    data[key] = l
                elif key in cm:
                    data[key] = JsonObjectFactory.create(cm[key], data[key])
        except KeyError:
            pass
        return cls(**data)


class Match(JsonObject):
    """ Match (JsonObject)

       Una representación pitón del objeto Match
    """
    def __init__(self, **kwargs):
        self.in_port = kwargs.get('in_port', None)
        self.in_phy_port = kwargs.get('in_phy_port', None)
        self.metadata = kwargs.get('metadata', None)
        self.tunnel_id = kwargs.get('tunnel_id', None)
        self.eth_dst = kwargs.get('eth_dst', None)
        self.eth_src = kwargs.get('eth_src', None)
        self.eth_type = kwargs.get('eth_type', None)
        self.ip_proto = kwargs.get('ip_proto', None)
        self.icmpv6_type = kwargs.get('icmpv6_type', None)
        self.ipv6_nd_sll = kwargs.get('ipv6_nd_sll', None)
        self.ipv6_nd_tll = kwargs.get('ipv6_nd_tll', None)
        self.vlan_vid = kwargs.get('vlan_vid', None)
        self.mode = kwargs.get('mode', None)
        self.vlan_pcp = kwargs.get('vlan_pcp', None)
        self.ip_dscp = kwargs.get('ip_dscp', None)
        self.ip_ecn = kwargs.get('ip_ecn', None)
        self.icmpv4_code = kwargs.get('icmpv4_code', None)
        self.icmpv6_code = kwargs.get('icmpv6_type', None)
        self.mpls_tc = kwargs.get('mpls_tc', None)
        self.mpls_bos = kwargs.get('mpls_bos', None)
        self.arp_op = kwargs.get('arp_op', None)
        self.ipv6_flabel = kwargs.get('ipv6_flabel', None)
        self.mpls_label = kwargs.get('mpls_label', None)
        self.pbb_isisd = kwargs.get('pbb_isisd', None)
        self.ipv4_src = kwargs.get('ipv4_src', None)
        self.ipv4_dst = kwargs.get('ipv4_dst', None)
        self.arp_spa = kwargs.get('arp_spa', None)
        self.arp_tpa = kwargs.get('arp_tpa', None)
        self.ipv6_src = kwargs.get('ipv6_src', None)
        self.ipv6_dst = kwargs.get('ipv6_dst', None)
        self.ipv6_nd_target = kwargs.get('ipv6_nd_target', None)
        self.tcp_src = kwargs.get('tcp_src', None)
        self.tcp_dst = kwargs.get('tcp_dst', None)
        self.udp_src = kwargs.get('udp_src', None)
        self.udp_dst = kwargs.get('udp_dst', None)
        self.sctp_src = kwargs.get('sctp_src', None)
        self.sctp_dst = kwargs.get('sctp_dst', None)
        self.icmpv4_type = kwargs.get('icmpv4_type', None)
        self.ipv6_exthdr = kwargs.get('ipv6_exthdr', None)

    def to_dict(self):
        """ to_dict (self)

           Crea una representación de la clase como un diccionario
            Anula el método de los padres como de todos los miembros de las variables
            esta clase son las cadenas

        """
        data = []
        attributes = [attr for attr in dir(self)
                      if not callable(getattr(self, attr)) and
                      not attr.startswith("__")]
        for attr in attributes:
            if getattr(self, attr):
                tmp = {}
                tmp[attr.__str__()] = getattr(self, attr)
                data.append(tmp)
        return data


class Action(JsonObject):
    """ Action (JsonObject)

        Una representación pitón del objeto Acción

    """
    def __init__(self, **kwargs):
        self.output = kwargs.get('output', None)
        self.copy_ttl_out = kwargs.get('copy_ttl_out', None)
        self.copy_ttl_in = kwargs.get('copy_ttl_in', None)
        self.set_mpls_ttl = kwargs.get('set_mpls_ttl', None)
        self.dec_mpls_ttls = kwargs.get('dec_mpls_ttls', None)
        self.push_vlan = kwargs.get('push_vlan', None)
        self.pop_vlan = kwargs.get('pop_vlan', None)
        self.push_mpls = kwargs.get('push_mpls', None)
        self.pop_mpls = kwargs.get('pop_mpls', None)
        self.set_queue = kwargs.get('set_queue', None)
        self.group = kwargs.get('group', None)
        self.set_nw_ttl = kwargs.get('set_nw_ttl', None)
        self.dec_nw_ttl = kwargs.get('dec_nw_ttl', None)
        self.set_field = kwargs.get('set_field', None)
        self.push_pbb = kwargs.get('push_pbb', None)
        self.pop_pbb = kwargs.get('pop_pbb', None)
        self.experimenter = kwargs.get('experimenter', None)
        self.data = kwargs.get('data', None)

    def to_dict(self):
        """ to_dict (self)

            Crea una representación de la clase como un diccionario
            Anula el método de los padres como de todos los miembros de las variables
            esta clase son las cadenas.

        """
        data = []
        attributes = [attr for attr in dir(self)
                      if not callable(getattr(self, attr)) and
                      not attr.startswith("__")]
        for attr in attributes:
            if attr == "output":
                output = getattr(self, attr)
                if type(output) == list:
                    for port in output:
                        tmp = {}
                        tmp[attr.__str__()] = port
                        data.append(tmp)
                elif output:
                    tmp = {}
                    tmp[attr.__str__()] = getattr(self, attr)
                    data.append(tmp)
            else:
                if getattr(self, attr):
                    tmp = {}
                    tmp[attr.__str__()] = getattr(self, attr)
                    data.insert(0, tmp)
        return data


class Instruction(JsonObject,):
    """ Instruction (JsonObject)

        Una representación pitón del objeto Instrucción

    """
    def __init__(self, **kwargs):
        self.clear_actions = kwargs.get('clear_actions', None)
        self.write_actions = kwargs.get('write_actions', [])
        self.apply_actions = kwargs.get('apply_actions', [])
        self.write_metadata = kwargs.get('write_metadata', None)
        self.mask = kwargs.get('mask', None)
        self.meter = kwargs.get('meter', None)
        self.experimenter = kwargs.get('experimenter', None)


class MeterStats(JsonObject):
    """ MeterStats (JsonObject)

       Una representación de python del objeto MeterStats.
t

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.flow_count = kwargs.get('flow_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.band_stats = kwargs.get('band_stats', [])


class BandStats(JsonObject):
    """ BandStats (JsonObject)

Una representación de python del objeto BandStats.

    """
    def __init__(self, **kwargs):
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)


class Meter(JsonObject):
    """ Meter (JsonObject)

       Una representación de python del objeto Meter.


    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.command = kwargs.get('command', None)
        self.flags = kwargs.get('flags', [])
        self.bands = kwargs.get('bands', [])


class MeterBand(JsonObject):
    """ MeterBand (JsonObject)

        Una representación de python del objeto MeterbAND.


    """
    def __init__(self, **kwargs):
        self.burst_size = kwargs.get('burst_size', None)
        self.rate = kwargs.get('rate', None)
        self.mtype = kwargs.get('mtype', None)
        self.prec_level = kwargs.get('prec_level', None)
        self.experimenter = kwargs.get('experimenter', None)


class Group(JsonObject):
    """ Group (JsonObject)

Una representación de python del objeto Group.

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.properties = kwargs.get('properties', None)
        self.ref_count = kwargs.get('ref_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.bucket_stats = kwargs.get('bucket_stats', [])
        self.type = kwargs.get('type', None)
        self.buckets = kwargs.get('buckets', [])


class Bucket(JsonObject):
    """ Bucket (JsonObject)

Una representación de python del objeto Buckets.

    """
    def __init__(self, **kwargs):
        self.weight = kwargs.get('weight', None)
        self.watch_group = kwargs.get('watch_group', None)
        self.watch_port = kwargs.get('watch_port', None)
        self.actions = kwargs.get('actions', [])


class Stats(JsonObject):
    """ Stats (JsonObject)

Una representación de python del objeto Stats.

    """
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.version = kwargs.get('version', None)
        self.port_stats = kwargs.get('port_stats', [])
        self.group_stats = kwargs.get('group_stats', [])
        self.meter_stats = kwargs.get('meter_stats', [])


class PortStats(JsonObject):
    """ PortStats (JsonObject)

Una representación de python del objeto PortStats.

    """
    def __init__(self, **kwargs):
        self.port_id = kwargs.get('id', None)
        self.rx_packets = kwargs.get('rx_packets', None)
        self.tx_packets = kwargs.get('tx_packets', None)
        self.rx_bytes = kwargs.get('rx_bytes', None)
        self.tx_bytes = kwargs.get('tx_bytes', None)
        self.rx_dropped = kwargs.get('rx_dropped', None)
        self.tx_dropped = kwargs.get('tx_dropped', None)
        self.rx_errors = kwargs.get('rx_errors', None)
        self.tx_errors = kwargs.get('tx_errors', None)
        self.collisions = kwargs.get('collisions', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.rx_crc_err = kwargs.get('rx_crc_err', None)
        self.rx_frame_err = kwargs.get('rx_frame_err', None)
        self.rx_over_err = kwargs.get('rx_over_err', None)


class GroupStats(JsonObject):
    """ GroupStats (JsonObject)

Una representación de python del objeto GroupStats.

    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.ref_count = kwargs.get('ref_count', None)
        self.packet_count = kwargs.get('packet_count', None)
        self.byte_count = kwargs.get('byte_count', None)
        self.duration_sec = kwargs.get('duration_sec', None)
        self.duration_nsec = kwargs.get('duration_nsec', None)
        self.bucket_stats = kwargs.get('bucket_stats', [])

# Network Services #


class Cluster(JsonObject):
    """ Cluster (JsonObject)

Una representación de python del objeto Cluster.

    """
    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', None)
        self.links = kwargs.get('links', [])


class Link(JsonObject):
    """ Link (JsonObject)

Una representación de python del objeto Link.

    """
    def __init__(self, **kwargs):
        self.src_dpid = kwargs.get('src_dpid', None)
        self.src_port = kwargs.get('src_port', None)
        self.dst_dpid = kwargs.get('dst_dpid', None)
        self.dst_port = kwargs.get('dst_port', None)
        self.info = kwargs.get('info', [])


class LinkInfo(JsonObject):
    """ LinkInfo (JsonObject)

Una representación de python del objeto LinkInfo.

    """
    def __init__(self, **kwargs):
        self.m_time = kwargs.get('m_time', None)
        self.u_time = kwargs.get('s_time', None)
        self.src_port_state = kwargs.get('s_pt_state', [])
        self.dst_port_state = kwargs.get('d_pt_state', [])
        self.link_type = kwargs.get('link_type', None)

# lldp_suppressed == list of LldpProperties


class LldpProperties(JsonObject):
    """ LldpProperties (JsonObject)

       Una representación de python del objeto LldpProperties 

    """
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.ports = kwargs.get('ports', [])


class Arp(JsonObject):
    """ Arp (JsonObject)

        Una representación de python del objeto Arp 

    """
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip', None)
        self.mac = kwargs.get('mac', None)
        self.vid = kwargs.get('vid', None)


class Node(JsonObject):
    """ Node (JsonObject)

        Una representación de python del objeto Node 

    """
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip', None)
        self.mac = kwargs.get('mac', None)
        self.vid = kwargs.get('vid', None)
        self.dpid = kwargs.get('dpid', None)
        self.port = kwargs.get('port', None)


class Path(JsonObject):
    """ Path (JsonObject)

        Una representación de python del objeto Path 

    """
    def __init__(self, **kwargs):
        self.cost = kwargs.get('cost', None)
        self.links = kwargs.get('links', [])


class LinkSync(JsonObject):
    """ LinkSync ()

       Una representación de python del objeto LinkSync 

    """

    def __init__(self, **kwargs):
        self.s_dpid = kwargs.get('s_dpid', None)
        self.s_port = kwargs.get('s_port', None)
        self.d_dpid = kwargs.get('d_dpid', None)
        self.d_port = kwargs.get('d_port', None)
        self.info = kwargs.get('info', None)


class ClusterSync(JsonObject):
    """ ClusterSync()

        Una representación de python del objeto ClusterSync 

    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.root = kwargs.get("root", None)
        self.nodes = kwargs.get("nodes", None)


class NodeSync(JsonObject):
    """ NodeSync()

       Una representación de python del objeto NodeSync 

    """
    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.links = kwargs.get('links', None)


class NodeLink(JsonObject):
    """ NodeLink()

        Una representación de python del objeto NodeLink

    """

    def __init__(self, **kwargs):
        self.s_dpid = kwargs.get('s_dpid', None)
        self.s_port = kwargs.get('s_port', None)
        self.d_dpid = kwargs.get('d_dpid', None)
        self.d_port = kwargs.get('d_port', None)
        self.s_pt_state = kwargs.get('s_pt_state', None)
        self.d_pt_state = kwargs.get('d_pt_state', None)


class NodeMessage(JsonObject):
    """ NodeMessage()

        Una representación de python del objeto NodeMessage 

    """

    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip', None)
        self.mac = kwargs.get('mac', None)
        self.vid = kwargs.get('vid', None)
        self.dpid = kwargs.get('dpid', None)
        self.port = kwargs.get('operation', None)

# Lldp_sync == a list of LldpProperties


class Btree(JsonObject):
    """ Btree()

        Una representación de python del objeto Btree 

    """

    def __init__(self, **kwargs):
        self.links = kwargs.get('links', [])
        self.costs = kwargs.get('costs', [])


class BtreeLink(JsonObject):
    """ BtreeLink()

       Una representación de python del objeto BtreeLink 

    """

    def __init__(self, **kwargs):
        self.dpid = kwargs.get('dpid', None)
        self.link = kwargs.get('link', [])


class TreeLink(JsonObject):
    """ TreeLink()

        Una representación de python del objeto TreeLink 

    """

    def __init__(self, **kwargs):
        self.s_dpid = kwargs.get('s_dpid', None)
        self.s_port = kwargs.get('s_port', None)
        self.d_dpid = kwargs.get('d_dpid', None)
        self.d_port = kwargs.get('d_port', None)


class Cost(JsonObject):
    """ Cost()

        Una representación de python del objetoe Cost 

    """

    def __init__(self, **kwargs):
        self.dpid = kwargs.get("dpid", None)
        self.cost = kwargs.get("cost", None)

# Core #


class AuditLogEntry(JsonObject):
    """ AuditLogEntry()

       Una representación de python del objeto AuditLogEnrty 

    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", [])
        self.system_uid = kwargs.get("system_uid", None)
        self.user = kwargs.get("user", None)
        self.ts = kwargs.get("ts", None)
        self.activity = kwargs.get("activity", None)
        self.description = kwargs.get("description", None)


class Alert(JsonObject):
    """ Alert()

        Una representación de python del objeto Alert 

    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.org = kwargs.get("org", None)
        self.ts = kwargs.get("ts", None)
        self.sev = kwargs.get("sev", None)
        self.state = kwargs.get("state", None)
        self.topic = kwargs.get("topic", None)
        self.desc = kwargs.get("desc", None)
        self.system_uid = kwargs.get("system_uid", None)


class AlertTopic(JsonObject):
    """ AlertTopic()

        Una representación de python del objeto AlertTopic 

    """

    def __init__(self, **kwargs):
        self.topic = kwargs.get("topic", None)
        self.org = kwargs.get("org", None)
        self.desc = kwargs.get("desc", None)


class AlertTopicListener(JsonObject):
    """ AlertTopicListener()

        Una representación de python del objeto AlertTopicListener 

    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("topic", None)
        self.app_id = kwargs.get("org", None)
        self.name = kwargs.get("desc", None)
        self.callbacks = kwargs.get("desc", [])


class Callback(JsonObject):
    """ Callback()

        Una representación de python del objeto Callback 

    """

    def __init__(self, **kwargs):
        self.topics = kwargs.get("topics", [])
        self.uri = kwargs.get("uri", None)


class Config(JsonObject):
    """ Config()

        Una representación de python del objeto Config 

    """

    def __init__(self, **kwargs):
        self.age_out_days = kwargs.get("age_out_days", [])
        self.trim_enabled = kwargs.get("trim_enabled", [])
        self.trim_interval_hours = kwargs.get("trim_interval_hours", [])


class ConfigItem(JsonObject):
    """ ConfigItem()

        Una representación de python del objeto ConfigItem 

    """

    def __init__(self, **kwargs):
        self.val = kwargs.get("val", None)
        self.def_val = kwargs.get("def_val", None)
        self.desc = kwargs.get("desc", None)


class SupportEntry(JsonObject):
    """ SupportEntry()

        Una representación de python del objeto SupportEntry 

    """

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", None)
        self.id = kwargs.get("id", None)
        self.content = kwargs.get("content", [])


class System(JsonObject):
    """ sistema """
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.version = kwargs.get("version", None)
        self.role = kwargs.get("role", None)
        self.core_data_version = kwargs.get("core_data_version", None)
        self.core_data_version_timestamp = kwargs.get(
            "core_data_version_timestamp", None
        )
        self.time = kwargs.get("time", None)
        self.self_ = kwargs.get("self_", None)
        self.status = kwargs.get("status", None)


class ControllerNode(JsonObject):
    """ EL nodo Controller  """

    def __init__(self, **kwargs):
        self.ip = kwargs.get("ip", None)
        self.name = kwargs.get("name", None)


class Region(JsonObject):
    """ La Región """
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.master = kwargs.get("master", None)
        self.slaves = kwargs.get("slaves", [])
        self.devices = kwargs.get("devices", [])


class Team(JsonObject):
    """ Team()

        Una representación de python del objeto Team 

    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.ip = kwargs.get("ip", None)
        self.version = kwargs.get("version")
        self.systems = kwargs.get("systems")


class TeamSystem(JsonObject):
    """ TeamSystems()

       Un objeto de Python para representar los sistemas que pertenecen a un equipo.

    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.ip = kwargs.get("name", None)
        self.priority = kwargs.get("name", None)


class Metric(JsonObject):
    """ Metric()

        Una representación de python del objeto Metric 

    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.app_id = kwargs.get("app_id", None)
        self.name = kwargs.get("name", None)
        self.type = kwargs.get("type", None)
        self.description = kwargs.get("description", None)
        self.primary_tag = kwargs.get("primary_tag", None)
        self.secondary_tag = kwargs.get("secondary_tag", None)
        self.jmx = kwargs.get("jmx", None)
        self.persistence = kwargs.get("persistence", None)
        self.summary_interval = kwargs.get("summary_interval", None)
        self.priming_value = kwargs.get("priming_value", None)


class MetricUpdate(JsonObject):
    """ Metric()

        Una representación de python del objeto MetricUpdate .

    """

    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.value = kwargs.get("value", None)
        self.int_value = kwargs.get("int_value", None)
        self.numerator = kwargs.get("numerator", None)
        self.denominator = kwargs.get("denominator", None)
        self.decrement = kwargs.get("decrement", None)
        self.increment = kwargs.get("increment", None)
        self.mark = kwargs.get("mark", None)
        self.type = kwargs.get("type", None)


class License(JsonObject):
    """ Licensia """
    def __init__(self, **kwargs):
        self.install_id = kwargs.get("install_id", None)
        self.serial_no = kwargs.get("serial_no", None)
        self.product = kwargs.get("product", None)
        self.license_metric = kwargs.get("license_metric", None)
        self.metric_qty = kwargs.get("metric_qty", None)
        self.license_type = kwargs.get("license_type", None)
        self.base_license = kwargs.get("base_license", None)
        self.creation_date = kwargs.get("creation_date", None)
        self.activated_date = kwargs.get("activated_date", None)
        self.expiry_date = kwargs.get("expiry_date", None)
        self.license_status = kwargs.get("license_status", None)
        self.deactivated_key = kwargs.get("deactivated_key", None)


class Packet(JsonObject):
    """ Packet()

       Una representación de python del objeto Packet.

    """

    def __init__(self, **kwargs):
        self.type = kwargs.get("type", None)
        self.uid = kwargs.get("uid", None)
        self.eth = kwargs.get("eth", None)
        self.ip = kwargs.get("ip", None)
        self.icmp = kwargs.get("icmp", None)
        self.ipv6 = kwargs.get("ipv6", None)
        self.icmpv6 = kwargs.get("icmpv6", None)
        self.tcp = kwargs.get("tcp", None)
        self.udp = kwargs.get("udp", None)
        self.dhcp = kwargs.get("dhcp", None)


class Ethernet(JsonObject):
    """ Ethernet()

       Un objeto python para representar la cabecera Ethernet.

    """

    def __init__(self, **kwargs):
        self.eth_src = kwargs.get("eth_src", None)
        self.eth_dst = kwargs.get("eth_dst", None)
        self.eth_type = kwargs.get("eth_type", None)
        self.vlan_vid = kwargs.get("vlan_vid", None)
        self.vlan_pcp = kwargs.get("vlan_pcp", None)


class Ip(JsonObject):
    """ Ip()

        Un objeto python para representar la cabecera IP.

    """

    def __init__(self, **kwargs):
        self.ipv4_src = kwargs.get("ipv4_src", None)
        self.ipv4_dst = kwargs.get("ipv4_dst", None)
        self.ip_proto = kwargs.get("ip_proto", None)
        self.ip_dscp = kwargs.get("ip_dscp", None)
        self.ip_ecn = kwargs.get("ip_ecn", None)
        self.ip_ident = kwargs.get("ip_ident", 0)


class Icmp(JsonObject):
    """ Icmp()

       Un objeto python para representar la cabecera ICMP

    """

    def __init__(self, **kwargs):
        self.icmp_code = kwargs.get("icmp_code", None)


class Ipv6(JsonObject):
    """ Ipv6()

        Un objeto python para representar la cabecera Ipv6.

    """

    def __init__(self, **kwargs):
        self.ipv6_src = kwargs.get("ipv4_src", None)
        self.ipv6_dst = kwargs.get("ipv4_dst", None)
        self.ip_proto = kwargs.get("ip_proto", None)
        self.ip_dscn = kwargs.get("ip_dscn", None)
        self.ip_hop_limit = kwargs.get("ip_hop_limit", None)


class Icmpv6(JsonObject):
    """ Icmp()

        Un objeto python para representar la cabecera Icmpv6.

    """

    def __init__(self, **kwargs):
        self.icmp_type_code = kwargs.get("icmp_code", None)
        self.is_sender_router = kwargs.get("is_sender_router", None)
        self.is_solicit_response = kwargs.get("is_solicit_response", None)
        self.override = kwargs.get("override", None)
        self.target_address = ('target_address', None)


class Tcp(JsonObject):
    """ Tcp()

        Una representación Pyhton de la cabecera TCP.

    """

    def __init__(self, **kwargs):
        self.tcp_dst = kwargs.get("tcp_dst", None)
        self.tcp_src = kwargs.get("tcp_src", None)


class Udp(JsonObject):
    """ Udp()

        Una representación Pyhton de la cabecera UDP.

    """

    def __init__(self, **kwargs):
        self.udp_dst = kwargs.get("udp_dst", None)
        self.udp_src = kwargs.get("udp_src", None)


class Dhcp(JsonObject):
    """ Dhcp()

        Una representación del pitón del mensaje DHCP.

    """

    def __init__(self, **kwargs):
        self.opcode = kwargs.get("opcode", None)
        self.boot_flags = kwargs.get("boot_flags", None)
        self.client_ip = kwargs.get("client_ip", None)
        self.your_client_ip = kwargs.get("your_client_ip", None)
        self.next_server_ip = kwargs.get("next_server_ip", None)
        self.relay_agent_ip = kwargs.get("relay_agent_ip", None)
        self.client_mac = kwargs.get("client_mac", None)
        self.options = kwargs.get("options", None)


class DhcpOptions(JsonObject):
    """ DhcpOptions()

        Una representación de Python de opciones DHCP.

    """
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", None)
        self.parameter_request_list = kwargs.get("parameter_request_list",
                                                 None)


class App(JsonObject):
    """ An app """
    def __init__(self, **kwargs):
        self.deployed = kwargs.get("deployed", None)
        self.desc = kwargs.get("desc", None)
        self.name = kwargs.get("name", None)
        self.state = kwargs.get("state", None)
        self.uid = kwargs.get("uid", None)
        self.vendor = kwargs.get("vendor", None)
        self.version = kwargs.get("version", None)


class AppHealth(JsonObject):
    """ Un objeto de health App """
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.deployed = kwargs.get("deployed", None)
        self.name = kwargs.get("name", None)
        self.state = kwargs.get("state", None)
        self.status = kwargs.get("status", None)


class MetricApp(JsonObject):
    """ Una aplicación con datos de medición en el disco """
    def __init__(self, **kwargs):
        self.app_id = kwargs.get("app_id", None)
        self.app_name = kwargs.get("app_name", None)


class MetricValues(JsonObject):
    """ Los valores de la métrica """
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", None)
        self.uid = kwargs.get("uid", None)
        self.datapoint_count = kwargs.get("datapoint_count", None)
        self.datapoints = kwargs.get("datapoints", [])


class DataPoint(JsonObject):
    """ Un punto de datos """
    def __init__(self, **kwargs):
        self.count = kwargs.get("count", None)
        self.milliseconds_span = kwargs.get("milliseconds_span", None)
        self.update_time = kwargs.get("upate_time", None)


class NextHop(JsonObject):
    def __init__(self, **kwargs):
        self.dpid = kwargs.get("dpid", None)
        self.out_port = kwargs.get("out_port", None)


class ControllerStats(JsonObject):
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.duration_ms = kwargs.get("duration_ms", None)
        self.lost = kwargs.get("lost", None)
        self.msg_in = kwargs.get("msg_in", None)
        self.msg_out = kwargs.get("msg_out", None)
        self.packet_in = kwargs.get("packet_in", None)
        self.packet_out = kwargs.get("packet_out", None)


class Counter(JsonObject):
    def __init__(self, **kwargs):
        self.packets = kwargs.get("packets", None)
        self.bytes = kwargs.get("bytes", None)


class Observation(JsonObject):
    def __init__(self, **kwargs):
        self.dpid = kwargs.get("dpid", None)
        self.type = kwargs.get("type", None)
        self.packet_uid = kwargs.get("packet_uid", None)
        self.status = kwargs.get("status", None)

CLASS_LIST = [s() for s in JsonObject.__subclasses__()]
