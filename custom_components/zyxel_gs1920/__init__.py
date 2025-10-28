from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches
from .const import DOMAIN, CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.options.get(CONF_HOST)
    version = entry.options.get(CONF_SNMP_VERSION, "2c")
    community = entry.options.get(CONF_COMMUNITY, "public")
    user = entry.options.get(CONF_USER)
    auth_key = entry.options.get(CONF_AUTH_KEY)
    priv_key = entry.options.get(CONF_PRIV_KEY)

    snmp_client = SNMPClient(
        host=host, version=version, community=community,
        user=user, auth_key=auth_key, priv_key=priv_key
    )

    hass.async_create_task(async_setup_sensors(hass, snmp_client, hass.helpers.entity_platform.async_add_entities))
    hass.async_create_task(async_setup_switches(hass, snmp_client, hass.helpers.entity_platform.async_add_entities))

    return True
