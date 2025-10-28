from pysnmp.hlapi.asyncio import *

class SNMPClient:
    def __init__(self, host, community="public", version="2c", user=None, auth_key=None, priv_key=None):
        self.host = host
        self.version = version
        self.community = community
        self.user = user
        self.auth_key = auth_key
        self.priv_key = priv_key

    async def get(self, oid):
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(self.community) if self.version=="2c" else UsmUserData(self.user, self.auth_key, self.priv_key),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return None
        for varBind in varBinds:
            return varBind[1]

    async def set(self, oid, value):
        iterator = setCmd(
            SnmpEngine(),
            CommunityData(self.community) if self.version=="2c" else UsmUserData(self.user, self.auth_key, self.priv_key),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), Integer(value))
        )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return False
        return True
