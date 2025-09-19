"""SNMP helper functions for Zyxel GS1920 integration."""

import logging

# Kompatible Importe für pysnmp 4.x und 7.x
try:
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
except ImportError:
    from pysnmp.hlapi.v3arch.asyncio import (
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

_LOGGER = logging.getLogger(__name__)


def test_snmpv3_connection_sync(config: dict) -> bool:
    """Testet eine SNMPv3 Verbindung synchron."""
    try:
        _LOGGER.debug("SNMPv3 Test gestartet mit Config: %s", config)

        iterator = getCmd(
            SnmpEngine(),
            UsmUserData(
                config["username"],
                config.get("auth_key"),
                config.get("priv_key"),
                authProtocol=usmHMACSHAAuthProtocol,
                privProtocol=usmAesCfb128Protocol,
            ),
            UdpTransportTarget((config["host"], int(config.get("port", 161)))),
            ContextData(),
            ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),  # sysDescr.0
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            _LOGGER.error("SNMP Fehler: %s", errorIndication)
            return False
        elif errorStatus:
            _LOGGER.error(
                "SNMP Fehlerstatus bei %s: %s",
                errorIndex,
                errorStatus.prettyPrint(),
            )
            return False
        else:
            for varBind in varBinds:
                _LOGGER.debug("SNMP Antwort: %s", " = ".join([x.prettyPrint() for x in varBind]))
            return True

    except Exception as e:
        _LOGGER.exception("SNMPv3 Verbindung fehlgeschlagen: %s", e)
        return False
