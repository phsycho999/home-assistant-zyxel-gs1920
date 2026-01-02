from pysnmp.hlapi.asyncio import (
    SnmpEngine, UdpTransportTarget, ContextData,
    UsmUserData, getCmd, setCmd, ObjectType, ObjectIdentity
)

class ZyxelSNMP:
    def __init__(self, host, user, auth_key, auth_proto, priv_key=None, priv_proto=None, port=161):
        self.host = host
        self.port = port
        self.user_data = UsmUserData(user, authKey=auth_key, authProtocol=auth_proto,
                                     privKey=priv_key, privProtocol=priv_proto)
        self.context = ContextData()
        self.engine = SnmpEngine()

    async def get_system_name(self):
        """Beispiel SNMP GET OID für System Name"""
        iterator = getCmd(self.engine, self.user_data,
                          UdpTransportTarget.create((self.host, self.port)),
                          self.context,
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')))
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return None
        return str(varBinds[0][1])

    async def set_poe(self, port_index: int, enable: bool):
        """PoE pro Port an/aus"""
        oid = f'1.3.6.1.4.1.890.1.9.2.1.6.{port_index}'  # Beispiel OID, prüfen!
        value = 1 if enable else 2  # Enable = 1, Disable = 2
        iterator = setCmd(self.engine, self.user_data,
                          UdpTransportTarget.create((self.host, self.port)),
                          self.context,
                          ObjectType(ObjectIdentity(oid), value))
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return False
        return True
