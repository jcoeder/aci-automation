## Step 1 - Clone repo and setup Python virtual environment

```
git clone https://github.com/jcoeder/aci-automation.git
cd aci-automation/provision_switch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2 - run provision_switch_serial.py

This script will allow the user to roam around the data center with a serial cable and set an OOB IP address to be used temporarily to upload the ACI image and reboot.  These assigned IP addresses are then added to the Ansible inventory file to be used by Ansible later. 

The file oob_addresses.txt needs updated to a list of temporary addresses to use to provision the switches.
The file provision-switch-serial.py needs updated to reflect the subnet and gateway for the switches as well as the local serial device

```
cd provision_switch
vi oob_addresses.txt
python provision-switch-serial.py
```
[![Watch the video](https://img.youtube.com/vi/e3FNTyLiByM/hqdefault.jpg)](https://youtu.be/e3FNTyLiByM)

## Step 3 - run provision_switch_aci.yml

This Ansible Playbook uses the inventory file generated by provision-switch-serial.py to connect to all the provisioned switches.  The playbook tells each switch to SCP to a server and pull the ACI firmware, set boot record, and reboot the switch so that it is ready to be added to the fabric.

```
ansible-playbook provision_switch_aci.yml
```
[![Watch the video](https://img.youtube.com/vi/ocwHZ4mxA44/hqdefault.jpg)](https://www.youtube.com/watch?v=ocwHZ4mxA44)
