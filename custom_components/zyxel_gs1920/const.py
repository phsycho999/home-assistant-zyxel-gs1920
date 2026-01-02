DOMAIN = "zyxel_gs1920"
DEFAULT_PORTS = 24
DEFAULT_SNMP_PORT = 161

PLATFORMS = ["sensor", "switch"]

# OIDs
OID_IF_OPER_STATUS = "1.3.6.1.2.1.2.2.1.8"  # Port up/down
OID_IF_ADMIN_STATUS = "1.3.6.1.2.1.2.2.1.7" # Port enable/disable
OID_POE_POWER_UP = "1.3.6.1.4.1.890.1.59.1.2.1.2"  # zyPoePsePowerUp
OID_POE_STATUS = "1.3.6.1.4.1.890.1.59.1.2.1.1"     # zyPoePsePortInfoPowerConsumption
