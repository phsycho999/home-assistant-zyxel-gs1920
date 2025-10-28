from pysnmp.hlapi.asyncio import *
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACSHAAuthProtocol, usmAesCfb128Protocol, ObjectType, ObjectIdentity, SnmpEngine, ContextData, UdpTransportTarget, Integer
from .const import *

# Ports abfragen
async def get_ports(host, username, auth_key="", priv_key=""):
    user = UsmUserData(username, auth_key, priv_key, authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol)
    transport = UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    ports = {}
    for port in range(1, DEFAULT_PORTS + 1):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            SnmpEngine(),
            user,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(f"{OID_IF_OPER_STATUS}.{port}"))
        )
        if not errorIndication and not errorStatus:
            ports[port] = int(varBinds[0][1])
        else:
            ports[port] = None
    return ports

# PoE Status abfragen
async def get_poe_status(host, username, auth_key="", priv_key=""):
    user = UsmUserData(username, auth_key, priv_key, authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol)
    transport = UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    poe_ports = {}
    for port in range(1, DEFAULT_PORTS + 1):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            SnmpEngine(),
            user,
            transport,
            ContextData(),
            ObjectType(ObjectIdentity(f"{OID_POE_STATUS}.{port}"))
        )
        if not errorIndication and not errorStatus:
            poe_ports[port] = int(varBinds[0][1]) > 0
        else:
            poe_ports[port] = None
    return poe_ports

# PoE Port ein-/ausschalten
async def set_poe_port(host, username, port, enable=True, auth_key="", priv_key=""):
    user = UsmUserData(username, auth_key, priv_key, authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol)
    transport = UdpTransportTarget.create((host, DEFAULT_SNMP_PORT))
    value = Integer(1 if enable else 2)
    errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
        SnmpEngine(),
        user,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(f"{OID_POE_POWER_UP}.{port}"), value)
    )
    return not (errorIndication or errorStatus)
