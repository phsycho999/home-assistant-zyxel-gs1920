from pysnmp.hlapi.asyncio import *

class SNMPClient:
    def __init__(self, host, community="public", version="2c", user=None, auth_key=None, priv_key=None):
        self.host = host
        self.community = community
        self.version = version
        self.user = user
        self.auth_key = auth_key
        self.priv_key = priv_key

    async def get(self, oid):
        if self.version in ["1", "2c"]:
            iterator = getCmd(SnmpEngine(),
                              CommunityData(self.community, mpModel=1 if self.version == "2c" else 0),
                              UdpTransportTarget((self.host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)))
        else:  # v3
            iterator = getCmd(SnmpEngine(),
                              UsmUserData(self.user, self.auth_key, self.priv_key),
                              UdpTransportTarget((self.host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)))
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return None
        return varBinds[0][1]

    async def set(self, oid, value):
        # Nur SNMP v2c/v3
        if self.version in ["1", "2c"]:
            iterator = setCmd(SnmpEngine(),
                              CommunityData(self.community, mpModel=1 if self.version == "2c" else 0),
                              UdpTransportTarget((self.host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid), Integer(value)))
        else:
            iterator = setCmd(SnmpEngine(),
                              UsmUserData(self.user, self.auth_key, self.priv_key),
                              UdpTransportTarget((self.host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid), Integer(value)))
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        return errorIndication is None and errorStatus == 0
