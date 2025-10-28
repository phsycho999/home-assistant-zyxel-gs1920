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
        """Get SNMP value (supports v2c & v3)."""
        if self.community:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=1),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
        else:
            # v3
            from pysnmp.hlapi import UsmUserData, UsmAuthProtocol, UsmPrivProtocol
            auth_proto = getattr(UsmAuthProtocol, self.auth_protocol, UsmAuthProtocol.NOAUTH)
            priv_proto = getattr(UsmPrivProtocol, self.priv_protocol, UsmPrivProtocol.NOPRIV)

            iterator = getCmd(
                SnmpEngine(),
                UsmUserData(self.user, self.auth_key, self.priv_key, authProtocol=auth_proto, privProtocol=priv_proto),
                UdpTransportTarget((self.host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return None
        return varBinds[0][1]

    def set(self, oid, value):
        """Set SNMP value (simplified for v2c)."""
        from pysnmp.hlapi import setCmd, CommunityData, SnmpEngine, UdpTransportTarget, ContextData, ObjectType, Integer, ObjectIdentity
        iterator = setCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            UdpTransportTarget((self.host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), Integer(value))
        )
        # return immediately (async handling optional)
        return iterator
