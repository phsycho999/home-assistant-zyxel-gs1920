import asyncio
from pysnmp.hlapi import *

async def snmp_get(host, community, oid, port=161):
    loop = asyncio.get_running_loop()

    def blocking_get():
        for (errInd, errStatus, errIndex, varBinds) in getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        ):
            if errInd:
                raise Exception(errInd)
            elif errStatus:
                raise Exception(f"{errStatus} at {errIndex}")
            return varBinds[0][1]

    return await loop.run_in_executor(None, blocking_get)


async def snmp_set(host, community, oid, value, port=161):
    loop = asyncio.get_running_loop()

    def blocking_set():
        for (errInd, errStatus, errIndex, varBinds) in setCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), value)
        ):
            if errInd:
                raise Exception(errInd)
            elif errStatus:
                raise Exception(f"{errStatus} at {errIndex}")
        return True

    return await loop.run_in_executor(None, blocking_set)
