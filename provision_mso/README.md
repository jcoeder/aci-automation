## Step 1 - Clone repo and setup Python virtual environment
```
git clone https://github.com/jcoeder/aci-automation.git
cd aci-automation/provision_mso
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2 - run mso_master_swarm_playbook.yml
This playbook deploys MSO AFTER an IP address has been set on each of the nodes.  The inventory file `hosts` needs to be updated and the PASSWORD in each playbook should be updated as well.
```
cd provision_mso
ansible-playbook mso_master_swarm_playbook.yml
```
[![Watch the video](https://img.youtube.com/vi/Yn32u6Q2QIs/hqdefault.jpg)](https://www.youtube.com/watch?v=Yn32u6Q2QIs)
