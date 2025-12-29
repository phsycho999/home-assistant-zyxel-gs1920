from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    setCmd,
    UsmUserData,
)
from pysnmp.proto.rfc1902 import Integer


class ZyxelSNMPClient:
    def __init__(self, host, username, auth_key, priv_key):
        self.engine = SnmpEngine()
        self.target = UdpTransportTarget((host, 161))
        self.context = ContextData()
        self.user = UsmUserData(username, auth_key, priv_key)

    async def get_ports(self):
        # Beispiel: Admin Status Port 1
        oid = "1.3.6.1.2.1.2.2.1.7.1"  # ifAdminStatus.1

        errorIndication, errorStatus, _, varBinds = await getCmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid)),
        )

        if errorIndication or errorStatus:
            raise Exception(errorIndication or errorStatus)

        return {
            "port1_admin": int(varBinds[0][1])
        }

    async def set_port_admin(self, port: int, enabled: bool):
        oid = f"1.3.6.1.2.1.2.2.1.7.{port}"
        value = Integer(1 if enabled else 2)

        await setCmd(
            self.engine,
            self.user,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid), value),
        )
