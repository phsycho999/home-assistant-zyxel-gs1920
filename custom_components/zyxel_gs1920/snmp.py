from pysnmp.hlapi.asyncio import *

class SNMPClient:
    def __init__(self, host, community, port=161):
        self.host = host
        self.community = community
        self.port = port

    async def get(self, oid):
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            UdpTransportTarget((self.host, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return None
        return int(varBinds[0][1])

    async def set(self, oid, value):
        iterator = setCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            UdpTransportTarget((self.host, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), Integer(value))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return False
        return True
