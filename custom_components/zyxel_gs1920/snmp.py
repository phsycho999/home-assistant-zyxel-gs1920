from pysnmp.hlapi import *

class SNMPClient:
    def __init__(self, host, port=161, version="2c", community="public",
                 user=None, auth_protocol=None, auth_key=None,
                 priv_protocol=None, priv_key=None):
        self.host = host
        self.port = port
        self.version = version
        self.community = community
        self.user = user
        self.auth_protocol = auth_protocol
        self.auth_key = auth_key
        self.priv_protocol = priv_protocol
        self.priv_key = priv_key

    def get_engine(self):
        if self.version in ["1", "2c"]:
            return CommunityData(self.community, mpModel=0 if self.version=="1" else 1)
        elif self.version == "3":
            auth_proto = {
                "MD5": usmHMACMD5AuthProtocol,
                "SHA": usmHMACSHAAuthProtocol
            }.get(self.auth_protocol, usmHMACSHAAuthProtocol)
            priv_proto = {
                "DES": usmDESPrivProtocol,
                "AES": usmAesCfb128Protocol
            }.get(self.priv_protocol, usmDESPrivProtocol)
            return UsmUserData(self.user, self.auth_key, self.priv_key,
                               authProtocol=auth_proto, privProtocol=priv_proto)
        else:
            raise ValueError("Unsupported SNMP version")

    async def get(self, oid):
        iterator = getCmd(SnmpEngine(),
                          self.get_engine(),
                          UdpTransportTarget((self.host, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid)))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication or errorStatus:
            return None
        return varBinds[0][1]

    async def set(self, oid, value):
        iterator = setCmd(SnmpEngine(),
                          self.get_engine(),
                          UdpTransportTarget((self.host, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(oid), Integer(value)))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication or errorStatus:
            return False
        return True
