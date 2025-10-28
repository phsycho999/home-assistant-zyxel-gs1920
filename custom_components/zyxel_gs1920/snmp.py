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
        if self.version == "2c":
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
        else:  # v3
            iterator = getCmd(
                SnmpEngine(),
                UsmUserData(self.user, self.auth_key, self.priv_key),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            return None
        elif errorStatus:
            return None
        else:
            for varBind in varBinds:
                return varBind[1]

    async def set(self, oid, value):
        if self.version == "2c":
            iterator = setCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), Integer(value))
            )
        else:  # v3
            iterator = setCmd(
                SnmpEngine(),
                UsmUserData(self.user, self.auth_key, self.priv_key),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), Integer(value))
            )
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return False
        return True
