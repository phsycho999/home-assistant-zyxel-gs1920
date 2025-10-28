from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import ZyxelPortSwitch, ZyxelPoESwitch
from .const import DEFAULT_PORTS
from homeassistant.helpers.entity_platform import async_add_entities

async def async_setup_entry(hass, entry):
    host = entry.data["host"]
    version = entry.data.get("snmp_version", "2c")
    community = entry.data.get("community", "public")
    user = entry.data.get("username")
    auth_protocol = entry.data.get("auth_protocol")
    auth_key = entry.data.get("auth_key")
    priv_protocol = entry.data.get("priv_protocol")
    priv_key = entry.data.get("priv_key")

    snmp = SNMPClient(host, version=version, community=community,
                      user=user, auth_protocol=auth_protocol, auth_key=auth_key,
                      priv_protocol=priv_protocol, priv_key=priv_key)

    # Sensoren
    await async_setup_sensors(hass, snmp, ports=DEFAULT_PORTS)

    # Switches
    switches = []
    for i in range(1, DEFAULT_PORTS + 1):
        switches.append(ZyxelPortSwitch(snmp, i))
        switches.append(ZyxelPoESwitch(snmp, i))
    hass.async_create_task(async_add_entities(switches))

    return True
