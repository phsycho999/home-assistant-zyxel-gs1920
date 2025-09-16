from pysnmp.hlapi import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    setCmd,
    Integer,
    usmHMACSHAAuthProtocol,
    usmHMACMD5AuthProtocol,
    usmAesCfb128Protocol,
    usmDESPrivProtocol,
)


def get_snmpv3(host, snmp_user, auth_protocol, auth_password, priv_protocol, priv_password, oid):
    """SNMPv3 GET request"""
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
    """SNMPv3 SET request"""
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
    """Test SNMPv3 connection to the switch."""
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            config["snmp_user"],
            config["auth_password"],
            config["priv_password"],
            authProtocol=usmHMACSHAAuthProtocol if config["auth_protocol"] == "SHA" else usmHMACMD5AuthProtocol,
            privProtocol=usmAesCfb128Protocol if config["priv_protocol"] == "AES" else usmDESPrivProtocol
        ),
        UdpTransportTarget((config["host"], 161)),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr OID
    )
    try:
        error_indication, error_status, error_index, var_binds = next(iterator)
        return error_indication is None and error_status is None
    except Exception:
        return False
