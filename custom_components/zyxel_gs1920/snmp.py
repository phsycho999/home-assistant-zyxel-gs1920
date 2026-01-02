import asyncio
from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    getCmd,
    setCmd,
    ObjectType,
    ObjectIdentity,
)
from .const import SECURITY_LEVELS

class ZyxelSNMP:
    def __init__(self, host, username, auth_key, priv_key, security_level="authPriv", port=161):
        self.engine = SnmpEngine()
        self.user = UsmUserData(username, auth_key, priv_key, security_level=security_level)
        self.target = UdpTransportTarget.create((host, port))
        self.context = ContextData()

    async def get(self, oid):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            self.engine, self.user, self.target, self.context, ObjectType(ObjectIdentity(oid))
        )
        if errorIndication:
            raise Exception(errorIndication)
        return varBinds[0][1]

    async def set(self, oid, value, value_type="Integer"):
        obj = ObjectType(ObjectIdentity(oid), value)
        errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
            self.engine, self.user, self.target, self.context, obj
        )
        if errorIndication:
            raise Exception(errorIndication)
        return varBinds[0][1]
