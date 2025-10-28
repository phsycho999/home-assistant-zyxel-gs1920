from pysnmp.hlapi.asyncio import *

class SNMPClient:
    def __init__(self, host, community=None, user=None, auth_protocol=None, auth_key=None, priv_protocol=None, priv_key=None):
        self.host = host
        self.community = community
        self.user = user
        self.auth_protocol = auth_protocol
        self.auth_key = auth_key
        self.priv_protocol = priv_protocol
        self.priv_key = priv_key

    async def get(self, oid):
        if self.community:
            # SNMPv2c
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
        else:
            # SNMPv3
            iterator = getCmd(
                SnmpEngine(),
                UsmUserData(self.user, self.auth_key, self.priv_key,
                            authProtocol=self.auth_protocol,
                            privProtocol=self.priv_protocol),
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
        # Nur SNMPv2c/3 set Unterstützung
        if self.community:
            iterator = setCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), Integer(value))
            )
        else:
            iterator = setCmd(
                SnmpEngine(),
                UsmUserData(self.user, self.auth_key, self.priv_key,
                            authProtocol=self.auth_protocol,
                            privProtocol=self.priv_protocol),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), Integer(value))
            )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        return errorIndication is None and errorStatus is None
