#!/usr/bin/env python
#
# *****APP para subir app a la controladora *****
#---------------------------------> Liberias generales
import argparse
import os
import hpsdnclient as hp
from hpsdnclient.error import NotFound

#---------------------------------> def. main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str,
                        help="The file to upload",
                        required=True)
    parser.add_argument('--app', type=str,
                        help="The application name e.g com.mango.hm",
                        required=True)

    args = parser.parse_args()

    upload(args.filename, args.app)

#---------------------------------> def. upload

def upload(filename, app):
#---------------------------------> variables que obtenemos mediante getters

    controller = os.getenv("SDNCTL")
    user = os.getenv("SDNUSER")
    password = os.getenv("SDNPASS")
#---------------------------------> Autentificación con la Api      

    auth = hp.XAuthToken(user=user, password=password, server=controller)
    api = hp.Api(controller=controller, auth=auth)

    running = is_running(api, app)

    if running:
        api.manage_app(app, "stop")
        api.uninstall_app(app)

    api.upload_app(filename)
    api.manage_app(app, "install")
    api.manage_app(app, "start")

#---------------------------------> def. is_running
def is_running(api, app):
    try:
        api.get_app_info(app)
    except NotFound:
        return False
    return True

if __name__ == "__main__":
    main()
