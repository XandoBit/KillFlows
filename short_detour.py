#!/usr/bin/env python
#
# *****APP para subir app a la controladora *****
#---------------------------------> Liberia general
import hpsdnclient as hp


#---------------------------------> def. main
def main():
    #initialize the api
    controller = '127.0.0.1'#---------------------------------> especifico ip controladora
#---------------------------------> Autentificación con la Api    
    auth = hp.XAuthToken(user='sdn', password='skyline', server=controller)
    api = hp.Api(controller=controller, auth=auth)

#---------------------------------> creamos un nuevo Objeto Match  
    match = hp.datatypes.Match(eth_type="ipv4", ipv4_src="10.0.0.1",
                               ipv4_dst="10.0.0.6",ip_proto="tcp",
                               tcp_dst="80")

#---------------------------------> Creamos las acciones del objeto
    output1 = hp.datatypes.Action(output="NORMAL")
    

#---------------------------------> Creamos los flujos 
    flow1 = hp.datatypes.Flow(priority=30000, idle_timeout=30,
                              match=match, actions=output1)
    flow2 = hp.datatypes.Flow(priority=30000, idle_timeout=30,
                              match=match, actions=output1)


    #api.add_datapaths('00:00:00:00:00:00:00:05')

#---------------------------------> enviamos los flujos a los switches    
    api.add_flows('00:00:00:00:00:00:00:02', flow1)
    api.add_flows('00:00:00:00:00:00:00:01', flow1)
    api.add_flows('00:00:00:00:00:00:00:03', flow1)

if __name__ == "__main__":
    main()
