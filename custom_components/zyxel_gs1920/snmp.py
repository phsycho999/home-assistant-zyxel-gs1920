from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, UsmUserData, UdpTransportTarget, ContextData, getCmd, setCmd, ObjectType, ObjectIdentity

class SNMPClient:
    def __init__(self, host, port=161, version="2c", community="public", user=None, auth_key=None, priv_key=None):
        self.host = host
        self.port = port
        self.version = version
        self.community = community
        self.user = user
        self.auth_key = auth_key
        self.priv_key = priv_key

    async def get(self, oid):
        if self.version in ["1", "2c"]:
            auth = CommunityData(self.community)
        else:
            auth = UsmUserData(self.user, self.auth_key, self.priv_key)

        iterator = getCmd(
            SnmpEngine(),
            auth,
            UdpTransportTarget((self.host, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            return None
        if errorStatus:
            return None
        for varBind in varBinds:
            return varBind[1]

    async def set(self, oid, value):
        if self.version in ["1", "2c"]:
            auth = CommunityData(self.community)
        else:
            auth = UsmUserData(self.user, self.auth_key, self.priv_key)

        iterator = setCmd(
            SnmpEngine(),
            auth,
            UdpTransportTarget((self.host, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), value)
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            return False
        if errorStatus:
            return False
        return True
