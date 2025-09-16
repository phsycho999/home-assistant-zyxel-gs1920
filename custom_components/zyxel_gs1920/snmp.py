from pysnmp.hlapi import *

def get_snmpv3(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, oid):
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            snmp_user,
            auth_password,
            priv_password,
            authProtocol=usmHMACSHAAuthProtocol if auth_protocol == "SHA" else usmHMACMD5AuthProtocol,
            privProtocol=usmAesCfb128Protocol if priv_protocol == "AES" else usmDESPrivProtocol
        ),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    error_indication, error_status, error_index, var_binds = next(iterator)
    if error_indication or error_status:
        return None
    return var_binds[0].prettyPrint().split('=')[-1].strip()


def set_snmpv3(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, oid, value):
    iterator = setCmd(
        SnmpEngine(),
        UsmUserData(
            snmp_user,
            auth_password,
            priv_password,
            authProtocol=usmHMACSHAAuthProtocol if auth_protocol == "SHA" else usmHMACMD5AuthProtocol,
            privProtocol=usmAesCfb128Protocol if priv_protocol == "AES" else usmDESPrivProtocol
        ),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), Integer(value))
    )
    error_indication, error_status, error_index, var_binds = next(iterator)
    return error_indication is None and error_status is None


async def test_snmpv3_connection(config):
    """Test SNMPv3 connection to the sw
