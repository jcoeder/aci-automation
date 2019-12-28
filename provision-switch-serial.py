# Update:
# ser.port
<<<<<<< HEAD
=======
# gateway and subnet
# list of IP addresses - 
>>>>>>> 903319378d40a1f7e37df83749c848f5cd23810d
# Use this to walk around the data center after rack and stack
# to set IP addresses to upload ACI Image
# About 40 seconds per switch, prevents human fat finger errors

import getpass
import serial
import time

<<<<<<< HEAD
=======
gateway = "192.168.254.1"
subnet =  "/24"

>>>>>>> 903319378d40a1f7e37df83749c848f5cd23810d
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

print("Provide password for switch.")
str_password = getpass.getpass()

ser = serial.Serial()
# ser.port = "/dev/ttyUSB0"
# ser.port = "/dev/tty.usbserial"
# ser.port = "/dev/ttyS2"
ser.port = '/dev/ttyS0'
ser.baudrate = 9600
# number of bits per bytes
ser.bytesize = serial.EIGHTBITS
# set parity check: no parity
ser.parity = serial.PARITY_NONE
# number of stop bits
ser.stopbits = serial.STOPBITS_ONE
# ser.timeout = None          #block read
ser.timeout = 1            #non-block read
# ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

with open("oob-addresses.txt") as f1:
    oob_addresses = f1.read().splitlines()

<<<<<<< HEAD
with open("oob-network.txt") as f2:
    oob_network = f2.read().splitlines()

=======
>>>>>>> 903319378d40a1f7e37df83749c848f5cd23810d
ser.open()

# Disable POAP
time.sleep(2)
ser.write(b'\n')
time.sleep(.5)
ser.write(b'\n')
time.sleep(.5)
ser.write(b'yes\n')
ser.write(b'yes\n')
ser.write(b'yes\n')
time.sleep(10)

# Enforce Secure Password
ser.write(b'yes\n')
time.sleep(3)

# Set admin password
byte_password = bytes(str_password)
ser.write(byte_password)
time.sleep(1.5)
ser.write(byte_password)
time.sleep(1.5)

# Do not enter basic configuration dialog
ser.write(b'no\n')
time.sleep(5)

# A couple returns, just to be safe
ser.write(b'\n')
time.sleep(1)
ser.write(b'\n')
time.sleep(1)

# Log in
ser.write(b'admin\n')
time.sleep(1)
ser.write(byte_password)
time.sleep(1)

# Enter configuration mode
ser.write(b'configure terminal\n')
time.sleep(1)

# Configure mgmt interface
ser.write(b'interface mgmt 0\n')
time.sleep(1)
ser.write(b'no shutdown\n')
time.sleep(1)
<<<<<<< HEAD
mgmt_ip = bytes('ip address ' + oob_addresses[0] + oob_network[0] + '\n', 'utf-8')
=======
mgmt_ip = bytes('ip address ' + oob_addresses[0] + subnet + '\n', 'utf-8')
>>>>>>> 903319378d40a1f7e37df83749c848f5cd23810d
ser.write(mgmt_ip)
time.sleep(1)
ser.write(b'exit\n')
time.sleep(1)

# Configure default route
ser.write(b'vrf context management\n')
time.sleep(1)
<<<<<<< HEAD
def_route = bytes('ip route 0.0.0.0/0 ' + oob_network[1] + ' vrf management\n', 'utf-8')
=======
def_route = bytes('ip route 0.0.0.0/0 ' + gateway + ' vrf management\n', 'utf-8')
>>>>>>> 903319378d40a1f7e37df83749c848f5cd23810d
ser.write(def_route)
time.sleep(1)

# Enable management features
ser.write(b'feature ssh')
time.sleep(1)
ser.write(b'feature scp')
time.sleep(1)
ser.write(b'feature sftp-server')
time.sleep(1)
ser.write(b'feature nxapi')
time.sleep(1)
ser.write(b'crypto key generate rsa\n')
time.sleep(1)

# Save the configuration
ser.write(b'copy run start\n')
time.sleep(8)

ser.close()

# Should probably write seek to find [nxos] and append after that
with open('hosts', 'a+') as f3:
    f3.writelines(oob_addresses[0] + '\n')

# Update inventory password to match what was supplied
with open('hosts', 'r') as f:
    hosts = f.read().splitlines()

hosts_pw_index = hosts.index('password=SWITCH_PROVISION_REPLACE')
hosts[hosts_pw_index] = 'password=' + str_password

with open('hosts', 'w') as f:
    for item in hosts:
        f.writelines("%s\n" % item)     
        
# Delete this IP address from available IP addresses so that it is not reused
del oob_addresses[0]

with open('oob-addresses.txt', 'w') as f1:
    for item in oob_addresses:
        f1.writelines("%s\n" % item)
