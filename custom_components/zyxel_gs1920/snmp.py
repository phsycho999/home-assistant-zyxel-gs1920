from pysnmp.hlapi.asyncio import *

class SNMPClient:
    def __init__(self, host, community="public", snmp_version="2c", user=None, auth_key=None, priv_key=None):
        self.host = host
        self.community = community
        self.snmp_version = snmp_version
        self.user = user
        self.auth_key = auth_key
        self.priv_key = priv_key

    async def get(self, oid):
        if self.snmp_version == "2c":
            return await self._get_v2c(oid)
        # SNMPv3 Implementation hier (optional)
        return None

    async def set(self, oid, value):
        if self.snmp_version == "2c":
            return await self._set_v2c(oid, value)
        return None

    async def _get_v2c(self, oid):
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            return None
        return varBinds[0][1]

    async def _set_v2c(self, oid, value):
        iterator = setCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), Integer(value))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            return None
        return varBinds[0][1]
