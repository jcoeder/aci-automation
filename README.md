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










### create-mso-backup.yml

This playbook should be imported into other playbooks that make changes to MSO to create a backup from before the changes

```
- name: Backup MSO
  import_playbook: create-mso-backup.yml
```
