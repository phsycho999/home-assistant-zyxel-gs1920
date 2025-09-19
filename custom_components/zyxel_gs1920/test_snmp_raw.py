from pysnmp.hlapi import SnmpEngine, UsmUserData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd, usmHMACSHAAuthProtocol, usmAesCfb128Protocol

host = "192.168.178.254"
user = "deinUser"
auth_protocol = "SHA"
auth_pass = "deinAuthPass"
priv_protocol = "AES"
priv_pass = "deinPrivPass"

iterator = getCmd(
    SnmpEngine(),
    UsmUserData(
        user,
        auth_pass,
        priv_pass,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol
    ),
    UdpTransportTarget((host, 161)),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr
)

error_indication, error_status, error_index, var_binds = next(iterator)

if error_indication or error_status:
    print("SNMPv3 Test Failed:", error_indication or error_status)
else:
    print("SNMPv3 Test Success:", var_binds[0].prettyPrint())
