from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .switch import ZyxelPortSwitch, ZyxelPoESwitch
from .sensor import ZyxelPoEPowerSensor

# ✅ OIDs aus MIB für den 24-Port GS1920
PORT_OID = "1.3.6.1.4.1.890.1.61.1.1.1.4"          # zyPortIntrusionLockState
POE_OID = "1.3.6.1.4.1.890.1.59.1.2.1.4"           # zyPoePseWideRangeDetection
POE_POWER_OID = "1.3.6.1.4.1.890.1.59.2.1.1"      # zyPoePsePortInfoPowerConsumption

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    host = entry.data["host"]
    community = entry.data["community"]
    ports = range(1, 25)  # 24 Ports

    port_switches = [ZyxelPortSwitch(host, community, port, f"{PORT_OID}.{port}") for port in ports]
    poe_switches = [ZyxelPoESwitch(host, community, port, f"{POE_OID}.{port}") for port in ports]
    poe_sensors = [ZyxelPoEPowerSensor(host, community, port, f"{POE_POWER_OID}.{port}", "PoE Power") for port in ports]

    async_add_entities(port_switches + poe_switches + poe_sensors)
