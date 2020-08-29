# aci-automation

```
git clone https://github.com/jcoeder/aci-automation.git
cd aci-automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## provision_switch/provision_switch_serial.py

This script will allow the user to roam around the data center with a serial cable and set an OOB IP address to be used temporarily to upload the ACI image and reboot.  These assigned IP addresses are then added to the Ansible inventory file to be used by Ansible later. 

The file oob_addresses.txt needs updated to a list of temporary addresses to use to provision the switches.
The file provision-switch-serial.py needs updated to reflect the subnet and gateway for the switches as well as the local serial device
```
vi oob_addresses.txt
python provision-switch-serial.py
```

[![Watch the video](https://img.youtube.com/vi/e3FNTyLiByM/hqdefault.jpg)](https://youtu.be/e3FNTyLiByM)

## provision_switch/provision_switch_aci.yml

This Ansible Playbook uses the inventory file generated by provision-switch-serial.py to connect to all the provisioned switches.  The playbook tells each switch to SCP to a server and pull the ACI firmware, set boot record, and reboot the switch so that it is ready to be added to the fabric.
```
ansible-playbook provision_switch_aci.yml
```

[![Watch the video](https://img.youtube.com/vi/ocwHZ4mxA44/hqdefault.jpg)](https://www.youtube.com/watch?v=ocwHZ4mxA44)


## lab_tools/simple-fabric-discovery.py

This script preforms a simple fabric discovery.  Each switch is given a prefix-name and nodeID.  Prefix-name is based on the role of the switch.  SPINE- for spine switches.  LEAF- for leaf switches.  nodeID is incremented 1 time for each switch added.  
```
python simple_fabric_discovery.py
```

[![Watch the video](https://img.youtube.com/vi/uX1M9PI6t1Y/hqdefault.jpg)](https://www.youtube.com/watch?v=uX1M9PI6t1Y)


### create-mso-backup.yml

This playbook should be imported into other playbooks that make changes to MSO to create a backup from before the changes

```
- name: Backup MSO
  import_playbook: create-mso-backup.yml
```


## main.py

This script will take an argument looking for the xlsx file to begin reading information from for the ACI Deployment.  Once it reads the information it will then create ansible variable files stored in the 'ansible variables' folder. The below example of how to use the script will include the file name that is bundled in the project as a template.

```
source venv/bin/activate
python main.py --aci_excel_sheet ACI_worksheet.xlsx
```
