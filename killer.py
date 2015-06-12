#!/usr/bin/env python
#
# ***********************************************-----APP externa de prueba para matar los flows------************************************************


#---------------------------------> APP de prueba para matar los flows <------------------------------------------------------------------------------
import argparse
import os
import hpsdnclient as hp
from hpsdnclient.datatypes import Flow, Match, Action

#---------------------------------> Librerias de  modulos certifi y requests <------------------------------------------------------------------------
import certifi
import requests
requests.packages.urllib3.disable_warnings()


#--------------------------------------------> Def. main <--------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()#-------------------------> Crear un objeto de programa de análisis y decirle qué argumentos esperar.
    parser.add_argument('--ip', type=str, #---------------------> El método add argument nos permite que esperamos algún argumento opcional,tipo string
                        help="Introduzca la IP ha matar.",#-----> Mensaje que nos aparece si el argumento no lo escribimos
                        required=True)#-------------------------> Es requerido, es decir, no podemos ejecutar el archivo sin escribir dicho argumento. 
                                      #-------------------------> En nuestro caso este argumento requerido es la Ip del host de origen.


    args = parser.parse_args()#------------>

    kill_flow(args.ip)#--------------------> llamada a kill_flow con la Ip ewspecificada por argumento. Por ejemplo: ./killer.py --ip 10.219.4.18




#------------------------------------------> Def. matar_flow <----------------------------------------------------------------------------------------
def kill_flow(ip):
#------------------------------------------> variables que obtenemos mediante getters
    controller = os.getenv("SDNCTL")#------> obtenemos la Ip del controlador
    user = os.getenv("SDNUSER")#-----------> obtenemos el nombre de usuario de acceso a la controladora
    password = os.getenv("SDNPASS")#-------> obtenemos la contraseña de acceso a la controladora
    #controller='127.0.0.1'
 #-----------------------------------------> Autentificación a la Api  
    auth = hp.XAuthToken(user='sdn', password='skyline', server='127.0.0.1')#----->
    api = hp.Api(controller='127.0.0.1', auth=auth)#------------------------------> obtenemos la Ip del controlador

#------------------------------------------> A continuación declkaramos las variables para identificar el host que queremos matar  a través del switch

    match = Match(eth_type="ipv4", ipv4_src=ip)#---------------------------------->especificamos la ip de origen y el tipo de ip
    action = Action(output=0)#---------------------------------------------------->paramos la acción a 0
    flow = Flow(priority=30000, match=match, actions=action, hard_timeout=100)#---->especificamos el flow y sus detalles en cada campos
    switches = api.get_datapaths()#----------------------------------------------->obtenemos los switches
    for s in switches:#----------------------------------------------------------->recorremos los switches
        api.add_flows(s.dpid, flow)#---------------------------------------------->añadimos el flow a 0 a dicho switch

if __name__ == "__main__":#------------------------------------------------------->condicional que compara la igualación
    main()#----------------------------------------------------------------------->llamada al main

