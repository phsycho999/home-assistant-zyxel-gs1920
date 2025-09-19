"""SNMP helper functions for Zyxel GS1920."""

from pysnmp.hlapi import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
)
from pysnmp.hlapi.auth import usmHMACSHAAuthProtocol, usmHMACMD5AuthProtocol
from pysnmp.hlapi.priv import usmAesCfb128Protocol, usmDESPrivProtocol
import logging

_LOGGER = logging.getLogger(__name__)

def test_snmpv3_connection_sync(config: dict) -> bool:
    """Test SNMPv3 connection to the switch."""
    auth_proto = usmHMACSHAAuthProtocol if config.get("auth_protocol", "SHA") == "SHA" else usmHMACMD5AuthProtocol
    priv_proto = usmAesCfb128Protocol if config.get("priv_protocol", "AES") == "AES" else usmDESPrivProtocol

    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(
            config["snmp_user"],
            config["auth_password"],
            config["priv_password"],
            authProtocol=auth_proto,
            privProtocol=priv_proto,
        ),
        UdpTransportTarget((config["host"], 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),  # sysDescr
    )

    try:
        error_indication, error_status, error_index, var_binds = next(iterator)
        if error_indication or error_status:
            _LOGGER.error("SNMPv3 test failed: %s", error_indication or error_status)
            return False
        return True
    except Exception as e:
        _LOGGER.exception("SNMPv3 test exception")
        return False
