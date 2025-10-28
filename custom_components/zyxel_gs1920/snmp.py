from pysnmp.hlapi.asyncio import *

async def snmp_get(host, oid, community="public"):
    iterator = getCmd(SnmpEngine(),
                      CommunityData(community, mpModel=1),
                      UdpTransportTarget((host, 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity(oid)))

    errorIndication, errorStatus, errorIndex, varBinds = await iterator
    if errorIndication or errorStatus:
        return None
    for varBind in varBinds:
        return int(varBind[1])

async def snmp_set(host, oid, value, community="private"):
    iterator = setCmd(SnmpEngine(),
                      CommunityData(community, mpModel=1),
                      UdpTransportTarget((host, 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity(oid), Integer(value)))

    errorIndication, errorStatus, errorIndex, varBinds = await iterator
    return not (errorIndication or errorStatus)
