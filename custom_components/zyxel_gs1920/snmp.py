"""SNMP helper functions for Zyxel GS1920 integration using PySNMP 7.x."""

import asyncio
from pysnmp.hlapi.v3arch import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd,
    set_cmd,
    usmHMACMD5AuthProtocol,
    usmNoPrivProtocol,
    usmDESPrivProtocol
)

async def test_snmpv3_connection(user_input: dict) -> bool:
    """Test SNMPv3 connection asynchronously."""
    host = user_input.get("host")
    username = user_input.get("username")
    auth_key = user_input.get("auth_key")
    priv_key = user_input.get("priv_key")

    snmp_engine = SnmpEngine()
    user_data = UsmUserData(
        userName=username,
        authKey=auth_key,
        privKey=priv_key,
        authProtocol=usmHMACMD5AuthProtocol,
        privProtocol=usmDESPrivProtocol if priv_key else usmNoPrivProtocol
    )
    target = UdpTransportTarget((host, 161))
    context = ContextData()

    # sysDescr.0 OID als Test
    iterator = get_cmd(
        snmp_engine,
        user_data,
        target,
        context,
        ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0"))
    )

    try:
        errorIndication, errorStatus, errorIndex, varBinds = await iterator
        if errorIndication or errorStatus:
            return False
        return True
    except Exception:
        return False

def test_snmpv3_connection_sync(user_input: dict) -> bool:
    """Synchronous wrapper to test SNMPv3 connection."""
    return asyncio.run(test_snmpv3_connection(user_input))
