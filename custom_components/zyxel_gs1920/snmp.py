import asyncio
from pysnmp.hlapi import (
    SnmpEngine, CommunityData, UsmUserData, UdpTransportTarget, ContextData,
    getCmd, setCmd, ObjectType, ObjectIdentity
)

class SNMPClient:
    def __init__(self, host, port=161, version="2c", community="public",
                 user=None, auth_key=None, priv_key=None):
        self.host = host
        self.port = port
        self.version = version
        self.community = community
        self.user = user
        self.auth_key = auth_key
        self.priv_key = priv_key

    def _get_auth(self):
        if self.version.lower() == "3":
            return UsmUserData(self.user, self.auth_key, self.priv_key)
        return CommunityData(self.community)

    async def get(self, oid):
        def sync_get():
            iterator = getCmd(
                SnmpEngine(),
                self._get_auth(),
                UdpTransportTarget((self.host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            if errorIndication or errorStatus:
                return None
            for varBind in varBinds:
                return varBind[1]
        return await asyncio.to_thread(sync_get)

    async def set(self, oid, value):
        def sync_set():
            iterator = setCmd(
                SnmpEngine(),
                self._get_auth(),
                UdpTransportTarget((self.host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid), value)
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            return not errorIndication and not errorStatus
        return await asyncio.to_thread(sync_set)
