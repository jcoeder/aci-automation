# aci-automation

```
git clone https://github.com/jcoeder/aci-automation.git
cd aci-automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## provision-switch-serial.py

This script will allow the user to roam around the data center with a serial cable and set an OOB IP address to be used temporarily to upload the ACI image and reboot.  These assigned IP addresses are then added to the Ansible inventory file to be used by Ansible later. 

```
source venv/bin/activate
python provision-switch-serial.py
```


## simple-fabric-discovery.py

This script preforms a simple fabric discovery.  Each switch is given a prefix-name and nodeID.  Prefix-name is based on the role of the switch.  SPINE- for spine switches.  LEAF- for leaf switches.  nodeID is incremented 1 time for each switch added.  

```
source venv/bin/activate
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
