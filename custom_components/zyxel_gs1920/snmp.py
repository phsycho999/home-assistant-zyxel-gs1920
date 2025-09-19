"""SNMP helper functions for Zyxel GS1920 using pysnmp 7.x AsyncIO."""
import asyncio
from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UsmUserData,
)
from pysnmp.hlapi.asyncio.auth import usmHMACSHAAuthProtocol, usmAesCfb128Protocol
from pysnmp.hlapi.asyncio import get

async def test_snmpv3_connection(host: str, username: str, auth_key: str, priv_key: str, port: int = 161):
    """Test SNMPv3 connection with pysnmp 7.x AsyncIO."""
    engine = SnmpEngine()
    user_data = UsmUserData(
        username,
        auth_key,
        priv_key,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )
    target = UdpTransportTarget((host, port))
    context = ContextData()
    oid = ObjectIdentity("1.3.6.1.2.1.1.1.0")  # sysDescr

    try:
        error_indication, error_status, error_index, var_binds = await get(
            engine,
            user_data,
            target,
            context,
            ObjectType(oid),
        )

        if error_indication:
            return False, str(error_indication)
        if error_status:
            return False, f"{error_status} at {error_index}"

        return True, str(var_binds[0][1])
    except Exception as e:
        return False, str(e)
    finally:
        await engine.transportDispatcher.closeDispatcher()

def test_snmpv3_connection_sync(host, username, auth_key, priv_key, port: int = 161):
    """Synchronous wrapper for testing outside Home Assistant."""
    return asyncio.get_event_loop().run_until_complete(
        test_snmpv3_connection(host, username, auth_key, priv_key, port)
    )
