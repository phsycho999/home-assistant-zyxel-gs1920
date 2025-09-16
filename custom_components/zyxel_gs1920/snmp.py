from pysnmp.hlapi import *

def get_snmp(host, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    error_indication, error_status, error_index, var_binds = next(iterator)
    if error_indication or error_status:
        return None
    return var_binds[0].prettyPrint().split('=')[-1].strip()

def set_snmp(host, community, oid, value):
    iterator = setCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), Integer(value))
    )
    error_indication, error_status, error_index, var_binds = next(iterator)
    return error_indication is None and error_status is None
