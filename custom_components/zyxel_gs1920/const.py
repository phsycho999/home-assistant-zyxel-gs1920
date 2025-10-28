DOMAIN = "zyxel_gs1920"
DEFAULT_PORTS = 24
DEFAULT_SNMP_PORT = 161

# OIDs für Ports
OID_IF_OPER_STATUS = "1.3.6.1.2.1.2.2.1.8"  # up/down
OID_IF_ADMIN_STATUS = "1.3.6.1.2.1.2.2.1.7"  # enable/disable

# OIDs für PoE
OID_POE_POWER_UP = "1.3.6.1.4.1.890.1.59.1.2.1.2"
OID_POE_STATUS = "1.3.6.1.4.1.890.1.59.1.2.1.1"
OID_POE_CONSUMPTION = "1.3.6.1.4.1.890.1.59.1.2.1.3"
OID_POE_CLASSIFICATION = "1.3.6.1.4.1.890.1.59.1.2.1.4"

# Config flow keys
CONF_HOST = "host"
CONF_COMMUNITY = "community"
CONF_SNMP_VERSION = "snmp_version"
CONF_USER = "user"
CONF_AUTH_KEY = "auth_key"
CONF_PRIV_KEY = "priv_key"
