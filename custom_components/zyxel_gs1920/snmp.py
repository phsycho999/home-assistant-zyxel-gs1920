from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    nextCmd,
    setCmd
)
from pysnmp.hlapi.asyncio import UsmUserData, usmHMACMD5AuthProtocol, usmAesCfb128Protocol
from pysnmp.proto.rfc1902 import Integer

async def get_ports(host, user_data):
    """Liste aller Ports mit Namen zurückgeben."""
    transport = UdpTransportTarget((host, 161))
    ports = []

    oid = ObjectIdentity("1.3.6.1.4.1.890.1.59.1.1.1.3")  # zyPortName
    errorIndication, errorStatus, errorIndex, varBinds = await nextCmd(
        SnmpEngine(),
        user_data,
        transport,
        ContextData(),
        ObjectType(oid),
        lexicographicMode=False
    )

    if not errorIndication:
        for varBind in varBinds:
            for oid_val, val in varBind:
                index = int(oid_val.prettyPrint().split('.')[-1])
                ports.append({"index": index, "name": str(val)})
    return ports

async def get_poe_status(host, user_data, port_index):
    transport = UdpTransportTarget((host, 161))
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        user_data,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(f"1.3.6.1.4.1.890.1.59.2.1.1.1.{port_index}"))
    )
    if errorIndication or errorStatus:
        return None
    return int(varBinds[0][1])

async def set_poe_port(host, user_data, port_index, power_on: bool):
    transport = UdpTransportTarget((host, 161))
    value = Integer(1 if power_on else 2)
    errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
        SnmpEngine(),
        user_data,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(f"1.3.6.1.4.1.890.1.59.1.2.1.2.{port_index}"), value)
    )
    return not (errorIndication or errorStatus)
