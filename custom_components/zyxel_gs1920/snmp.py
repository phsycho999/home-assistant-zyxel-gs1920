from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd,
    set_cmd,
)
from pysnmp.hlapi.v3arch import (
    usmHMACMD5AuthProtocol,
    usmDESPrivProtocol,
)


class ZyxelSNMP:
    def __init__(self, host, username, auth_key, priv_key):
        self.engine = SnmpEngine()
        self.user = UsmUserData(
            username,
            authKey=auth_key,
            privKey=priv_key,
            authProtocol=usmHMACMD5AuthProtocol,
            privProtocol=usmDESPrivProtocol,
        )
        self.target = UdpTransportTarget((host, 161))
        self.context = ContextData()

    async def get(self, oid):
        err, stat, _, binds = await get_cmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid)),
        )
        if err or stat:
            raise RuntimeError(err or stat)
        return int(binds[0][1])

    async def set(self, oid, value):
        err, stat, _, _ = await set_cmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid), value),
        )
        if err or stat:
            raise RuntimeError(err or stat)
