import asyncio
from pysnmp.hlapi.asyncio import *

class ZyxelSNMP:
    """Handle SNMP communication."""

    def __init__(self, host, username, auth_key, priv_key=None):
        self.host = host
        self.username = username
        self.auth_key = auth_key
        self.priv_key = priv_key

    async def get_port_status(self):
        """Return the port status."""
        user = UsmUserData(self.username, self.auth_key, self.priv_key)
        target = UdpTransportTarget.create((self.host, 161))
        context = ContextData()

        # Beispiel OID für System Name
        oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))

        iterator = getCmd(SnmpEngine(), user, target, context, oid)

        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            raise Exception(errorIndication)
        elif errorStatus:
            raise Exception(f"{errorStatus.prettyPrint()} at {errorIndex}")

        return {str(varBinds[0][0]): str(varBinds[0][1])}

    async def set_port_poe(self, port: int, enable: bool):
        """Enable or disable POE on a port."""
        user = UsmUserData(self.username, self.auth_key, self.priv_key)
        target = UdpTransportTarget.create((self.host, 161))
        context = ContextData()

        # Beispiel OID für POE Port Status, musst du anpassen
        oid = ObjectType(ObjectIdentity(f'1.3.6.1.2.1.105.1.1.1.3.{port}'), Integer(enable))

        iterator = setCmd(SnmpEngine(), user, target, context, oid)
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication:
            raise Exception(errorIndication)
        elif errorStatus:
            raise Exception(f"{errorStatus.prettyPrint()} at {errorIndex}")

        return True
