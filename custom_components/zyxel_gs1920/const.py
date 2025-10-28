DOMAIN = "zyxel_gs1920"
DEFAULT_PORTS = 24  # Anzahl Ports auf deinem Switch
DEFAULT_SNMP_PORT = 161

# OIDs für normale Ports
OID_IF_OPER_STATUS = "1.3.6.1.2.1.2.2.1.8"  # Port up/down
OID_IF_ADMIN_STATUS = "1.3.6.1.2.1.2.2.1.7"  # Port enable/disable

# OIDs für PoE (aus ZYXEL-POWER-ETHERNET-MIB)
OID_POE_POWER_UP = "1.3.6.1.4.1.890.1.59.1.2.1.2"  # zyPoePsePowerUp
OID_POE_STATUS = "1.3.6.1.4.1.890.1.59.1.2.1.1"  # zyPoePsePortInfoPowerConsumption (0=off, >0=on)
