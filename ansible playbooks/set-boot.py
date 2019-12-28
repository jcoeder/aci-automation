#!./venv/bin/python

from netmiko import ConnectHandler
import sys

device = {
'device_type': 'cisco_nxos',
'host': sys.argv[1],
'username': sys.argv[2],
'password': sys.argv[3],
}

filename = sys.argv[4]

net_connect = ConnectHandler(**device)
net_connect.send_command('conf t\n', expect_string=r'config')
net_connect.send_command('boot aci bootflash:' + filename + '\n', expect_string=r'Warning')
net_connect.send_command('y\n', expect_string=r'config')
