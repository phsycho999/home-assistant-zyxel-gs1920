from pysnmp.hlapi import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol,
)


def snmp_test_connection(host, username, auth_key, priv_key):
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            username,
            auth_key,
            priv_key,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol,
        ),
        UdpTransportTarget((host, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),  # sysDescr
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        raise RuntimeError(errorIndication)
    if errorStatus:
        raise RuntimeError(errorStatus.prettyPrint())

    return True
