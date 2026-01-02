from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    setCmd,
    usmHMACMD5AuthProtocol,
    usmDESPrivProtocol,
)


class ZyxelSNMP:
    def __init__(self, host, username, auth_key, priv_key):
        self.engine = SnmpEngine()
        self.user = UsmUserData(
            userName=username,
            authKey=auth_key,
            privKey=priv_key,
            authProtocol=usmHMACMD5AuthProtocol,
            privProtocol=usmDESPrivProtocol,
        )
        self.target = UdpTransportTarget((host, 161))
        self.context = ContextData()

    async def get(self, oid: str):
        error_indication, error_status, _, var_binds = await getCmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid)),
        )

        if error_indication or error_status:
            raise RuntimeError(f"SNMP GET failed: {error_indication}")

        return var_binds[0][1]

    async def set(self, oid: str, value):
        error_indication, error_status, _, _ = await setCmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid), value),
        )

        if error_indication or error_status:
            raise RuntimeError(f"SNMP SET failed: {error_indication}")
