from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UsmUserData,
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    Integer,
    getCmd,
    setCmd,
)
from .const import *


async def get_ports(host, username, auth_key="", priv_key=""):
    """Abfrage des Portstatus (up/down) aller Ports."""
    user = UsmUserData(
        username,
        auth_key,
        priv_key,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )
    transport = await UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    ports = {}
    for port in range(1, DEFAULT_PORTS + 1):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            SnmpEngine(),
            user,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(f"{OID_IF_OPER_STATUS}.{port}")),
        )
        if errorIndication or errorStatus:
            ports[port] = None
        else:
            ports[port] = int(varBinds[0][1])
    return ports


async def get_poe_status(host, username, auth_key="", priv_key=""):
    """Abfrage des PoE-Status aller Ports."""
    user = UsmUserData(
        username,
        auth_key,
        priv_key,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )
    transport = await UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    poe_ports = {}
    for port in range(1, DEFAULT_PORTS + 1):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            SnmpEngine(),
            user,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(f"{OID_POE_STATUS}.{port}")),
        )
        if errorIndication or errorStatus:
            poe_ports[port] = None
        else:
            poe_ports[port] = int(varBinds[0][1]) > 0
    return poe_ports


async def set_poe_port(host, username, port, enable=True, auth_key="", priv_key=""):
    """PoE-Port ein- oder ausschalten."""
    user = UsmUserData(
        username,
        auth_key,
        priv_key,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )
    transport = await UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    value = Integer(1 if enable else 2)

    errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
        SnmpEngine(),
        user,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(f"{OID_POE_POWER_UP}.{port}"), value),
    )

    return not (errorIndication or errorStatus)
