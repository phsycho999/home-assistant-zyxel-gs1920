from .const import DOMAIN, CONF_HOST, CONF_COMMUNITY, CONF_SNMP_VERSION, CONF_USER, CONF_AUTH_KEY, CONF_PRIV_KEY
from .snmp import SNMPClient
from .sensor import async_setup_sensors
from .switch import async_setup_switches

async def async_setup_entry(hass, entry):
    # SNMP Client erstellen
    host = entry[CONF_HOST]
    version = entry.get(CONF_SNMP_VERSION, "2c")
    community = entry.get(CONF_COMMUNITY, "public")
    user = entry.get(CONF_USER)
    auth_key = entry.get(CONF_AUTH_KEY)
    priv_key = entry.get(CONF_PRIV_KEY)

    snmp_client = SNMPClient(
        host=host,
        version=version,
        community=community,
        user=user,
        auth_key=auth_key,
        priv_key=priv_key
    )

    # Sensoren und Switches registrieren
    hass.async_create_task(
        async_setup_sensors(hass, snmp_client, lambda entities: hass.helpers.entity_platform.async_add_entities(entities))
    )
    hass.async_create_task(
        async_setup_switches(hass, snmp_client, lambda entities: hass.helpers.entity_platform.async_add_entities(entities))
    )
    return True

async def async_setup(hass, config):
    return True
