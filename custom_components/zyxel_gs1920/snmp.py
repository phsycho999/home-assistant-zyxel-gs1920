import asyncio
from pysnmp.hlapi.asyncio import (
    SnmpEngine,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
)
from pysnmp.hlapi.auth import UsmUserData
from pysnmp.hlapi.security import (
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol,
)


async def test_snmpv3_connection(host, port, user, auth_key, priv_key):
    """
    Testet eine SNMPv3-Verbindung asynchron.
    Gibt True zurück, wenn die Verbindung erfolgreich ist, sonst False.
    """
    try:
        engine = SnmpEngine()
        auth = UsmUserData(
            user,
            auth_key,
            priv_key,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol,
        )

        target = UdpTransportTarget((host, port), timeout=2.0, retries=1)
        context = ContextData()

        # Beispiel: Systembeschreibung abfragen (MIB-2 sysDescr)
        oid = ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0"))

        error_indication, error_status, error_index, var_binds = await getCmd(
            engine, auth, target, context, oid
        )

        if error_indication:
            return False, str(error_indication)
        elif error_status:
            return False, f"{error_status.prettyPrint()} at {error_index}"
        else:
            return True, f"{var_binds[0][1]}"
    except Exception as e:
        return False, str(e)


def test_snmpv3_connection_sync(host, port, user, auth_key, priv_key):
    """
    Sync-Wrapper für Tests außerhalb von Home Assistant.
    """
    return asyncio.get_event_loop().run_until_complete(
        test_snmpv3_connection(host, port, user, auth_key, priv_key)
    )
