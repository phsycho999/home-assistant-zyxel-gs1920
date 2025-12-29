from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    ContextData,
    UdpTransportTarget,
    ObjectType,
    ObjectIdentity,
    getCmd,
    nextCmd,
    setCmd,
    UsmUserData,
)
from pysnmp.proto.rfc1902 import Integer


def build_user(username, auth_key, priv_key):
    return UsmUserData(username, auth_key, priv_key)


async def get_ports(host, user):
    transport = UdpTransportTarget((host, 161))
    ports = {}

    oid = ObjectIdentity(OID_PORT_NAME)

    async for errorIndication, errorStatus, _, varBinds in nextCmd(
        SnmpEngine(),
        user,
        transport,
        ContextData(),
        ObjectType(oid),
        lexicographicMode=False,
    ):
        if errorIndication or errorStatus:
            break

        for oid_val, val in varBinds:
            idx = int(oid_val.prettyPrint().split(".")[-1])
            ports[idx] = str(val)

    return ports


async def get_poe_status(host, user, port):
    transport = UdpTransportTarget((host, 161))
    oid = f"{OID_POE_STATUS}.{port}"

    errorIndication, errorStatus, _, varBinds = await getCmd(
        SnmpEngine(),
        user,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    if errorIndication or errorStatus:
        return None

    return int(varBinds[0][1])


async def set_poe(host, user, port, enable: bool):
    transport = UdpTransportTarget((host, 161))
    value = Integer(1 if enable else 2)

    oid = f"{OID_POE_ENABLE}.{port}"

    errorIndication, errorStatus, _, _ = await setCmd(
        SnmpEngine(),
        user,
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(oid), value),
    )

    return not (errorIndication or errorStatus)
