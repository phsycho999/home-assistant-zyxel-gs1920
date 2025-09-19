import asyncio
from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    UsmUserData,
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol,
)

async def test_snmpv3_connection(host: str, user: str, auth_key: str, priv_key: str, port: int = 161) -> (bool, str):
    """Testet eine SNMPv3-Verbindung asynchron."""
    engine = SnmpEngine()

    user_data = UsmUserData(
        user,
        auth_key,
        priv_key,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )

    target = UdpTransportTarget((host, port))
    context = ContextData()
    oid = ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0"))  # sysDescr

    try:
        error_indication, error_status, error_index, var_binds = await getCmd(
            engine, user_data, target, context, oid
        )

        if error_indication:
            return False, str(error_indication)
        elif error_status:
            return False, f"{error_status.prettyPrint()} at {error_index}"
        else:
            return True, str(var_binds[0][1])
    except Exception as e:
        return False, str(e)
    finally:
        await engine.transportDispatcher.closeDispatcher()


def test_snmpv3_connection_sync(host, user, auth_key, priv_key, port: int = 161):
    """Sync-Wrapper, z.B. für Tests außerhalb von HA."""
    return asyncio.get_event_loop().run_until_complete(
        test_snmpv3_connection(host, user, auth_key, priv_key, port)
    )
