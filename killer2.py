#!/usr/bin/env python
#
# ******APP externa de prueba para matar los flows ******


#---------------------------------> APP de prueba para matar los flows 
import argparse
import os
import hpsdnclient as hp
from hpsdnclient.datatypes import Flow, Match, Action

#---------------------------------> Librerias de  modulos certifi y requests
import certifi
import requests
requests.packages.urllib3.disable_warnings()


#---------------------------------> def. main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip1', type=str,
                        help="Introduzca la IP del host 1 ha matar.",
                        required=True,'--ip2', type=str,
                        help="Introduzca la IP  del host 2 ha matar.",
                        required=True)

    args = parser.parse_args()
    args2 = parser.parse_args()

    kill_flow(args.ip,args2.ip)

#---------------------------------> def. matamos el flow
def kill_flow(ip,ip2):
#---------------------------------> variables que obtenemos mediante getters
    controller = os.getenv("SDNCTL")
    user = os.getenv("SDNUSER")
    password = os.getenv("SDNPASS")
    #controller='127.0.0.1'
 #---------------------------------> Autentificación a la Api  
    auth = hp.XAuthToken(user='sdn', password='skyline', server='127.0.0.1')
    api = hp.Api(controller='127.0.0.1', auth=auth)

#---------------------------------> Variables para identificar el host que quertemos matar

    match = Match(eth_type="ipv4", ipv4_src=ip)#---->especificamos la ip de origen y el tipo de ip
    match2 = Match(eth_type="ipv4", ipv4_src=ip)#---->especificamos la ip de origen y el tipo de ip
    action = Action(output=0)#---->paramos la acción a 0
    flow = Flow(priority=30000, match=match, actions=action, hard_timeout=30)#---->especificamos el flow y sus detalles en cada campos
    flow2 = Flow(priority=30000, match=match2, actions=action, hard_timeout=30)
    switches = api.get_datapaths()#---->obtenemos los switches
    for s in switches:#---->recorremos los switches
        api.add_flows(s.dpid, flow)#---->añadimos el flow a 0 a dicho switch
    for x in datapaths:#---->recorremos los switches
        api.add_flows(x.dpid, flow2)#---->añadimos el flow a 0 a dicho switch

if __name__ == "__main__":
    main()

