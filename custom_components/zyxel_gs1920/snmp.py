"""SNMP helper functions for Zyxel GS1920."""
from pysnmp.hlapi.asyncio import SnmpEngine, getCmd, setCmd, nextCmd, UsmUserData
from pysnmp.hlapi import ObjectType, ObjectIdentity, UdpTransportTarget, Integer
from pysnmp.hlapi.usm import usmHMACMD5AuthProtocol, usmAesCfb128Protocol

async def get_ports(host, user_data):
    """Return list of ports with their index and name."""
    transport = UdpTransportTarget((host, 161))
    ports = []

    errorIndication, errorStatus, errorIndex, varBinds = await nextCmd(
        SnmpEngine(),
        user_data,
        transport,
        contextData=None,
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.59.1.1.1.3')),  # zyPortName
        lexicographicMode=False
    )

    if errorIndication:
        return ports

    for varBind in varBinds:
        for oid_val, val in varBind:
            port_index = int(oid_val.prettyPrint().split('.')[-1])
            ports.append({"index": port_index, "name": str(val)})

    return ports

async def get_poe_status(host, user_data, port_index):
    """Get PoE status of a port."""
    transport = UdpTransportTarget((host, 161))
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        user_data,
        transport,
        contextData=None,
        ObjectType(ObjectIdentity(f'{OID_POE_STATUS}.{port_index}'))
    )
    if errorIndication or errorStatus:
        return None
    return int(varBinds[0][1])

async def set_poe_port(host, user_data, port_index, power_on: bool):
    """Enable or disable PoE on a port."""
    transport = UdpTransportTarget((host, 161))
    value = Integer(1 if power_on else 2)
    errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
        SnmpEngine(),
        user_data,
        transport,
        contextData=None,
        ObjectType(ObjectIdentity(f'{OID_POE_POWER_UP}.{port_index}'), value)
    )
    return not (errorIndication or errorStatus)
