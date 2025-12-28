# snmp.py
from pysnmp.hlapi.asyncio import *
from pysnmp.hlapi.v3.usm import usmHMACMD5AuthProtocol, usmAesCfb128Protocol
from pysnmp.hlapi import SnmpEngine, ContextData, UdpTransportTarget, ObjectType, ObjectIdentity, Integer

# OIDs für Zyxel GS1920
OID_ZYPORT_NAME = "1.3.6.1.4.1.890.1.59.1.1.1.3"  # zyPortName
OID_POE_POWER = "1.3.6.1.4.1.890.1.59.1.2.1.2"    # zyPoePsePowerUp
OID_POE_STATUS = "1.3.6.1.4.1.890.1.59.1.2.1.1"   # zyPoePsePortInfoPowerConsumption

async def get_ports(host, user_data):
    """Liste aller Ports zurückgeben."""
    ports = []
    async for (errorIndication,
               errorStatus,
               errorIndex,
               varBinds) in nextCmd(
                    SnmpEngine(),
                    user_data,
                    UdpTransportTarget((host, 161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(OID_ZYPORT_NAME)),
                    lexicographicMode=False
               ):
        if errorIndication or errorStatus:
            break
        for varBind in varBinds:
            for oid_val, val in varBind:
                port_index = int(oid_val.prettyPrint().split('.')[-1])
                ports.append({"index": port_index, "name": str(val)})
    return ports

async def set_poe_port(host, user_data, port_index, power_on: bool):
    """Schaltet PoE eines Ports ein/aus."""
    value = Integer(1 if power_on else 2)  # 1=on, 2=off
    errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
        SnmpEngine(),
        user_data,
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(f"{OID_POE_POWER}.{port_index}"), value)
    )
    if errorIndication or errorStatus:
        return False
    return True

async def get_poe_status(host, user_data, port_index):
    """Liest PoE-Status eines Ports."""
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        user_data,
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(f"{OID_POE_STATUS}.{port_index}"))
    )
    if errorIndication or errorStatus:
        return None
    # Wenn >0 → PoE aktiv
    return int(varBinds[0][1]) > 0
