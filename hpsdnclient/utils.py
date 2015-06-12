#!/usr/bin/env python
#
# ******Fichero de utils ******

""" Useful utilities """

MAC = 12
DPID = 16


def string_to_hex(st, length):
    """ Convierte una cadena como 00:00 en hexadecimal 0x0000 formato"""
    tmp = '{0:#x}'.format(int(st.replace(':', '').lstrip('0'), length))
    return tmp


def hex_to_string(hx, length):
    """Convierte un número hexadecimal 0x0000 desde un formato 00:00"""
    tmp = hx.lstrip('0x').zfill(length)
    tmp = ':'.join(a+b for a, b in zip(tmp[::2], tmp[1::2]))
    return tmp
