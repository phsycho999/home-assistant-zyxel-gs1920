DOMAIN = "zyxel_gs1920"
DEFAULT_PORTS = 24  # Anzahl Ports auf deinem Switch
DEFAULT_SNMP_PORT = 161

# SNMP OIDs
OID_IF_OPER_STATUS = "1.3.6.1.2.1.2.2.1.8"       # Port up/down
OID_IF_ADMIN_STATUS = "1.3.6.1.2.1.2.2.1.7"     # Port enable/disable
OID_POE_POWER_UP = "1.3.6.1.4.1.890.1.59.1.2.1.2"  # PoE ein/aus
OID_POE_STATUS = "1.3.6.1.4.1.890.1.59.1.2.1.1"     # PoE Status
OID_POE_CONSUMPTION = "1.3.6.1.4.1.890.1.59.1.2.1.3" # PoE Verbrauch
OID_POE_CLASSIFICATION = "1.3.6.1.4.1.890.1.59.1.2.1.4" # PoE Klasse

# Config Flow Keys
CONF_HOST = "host"
CONF_COMMUNITY = "community"
CONF_SNMP_VERSION = "snmp_version"
CONF_USER = "user"
CONF_AUTH_KEY = "auth_key"
CONF_PRIV_KEY = "priv_key"
