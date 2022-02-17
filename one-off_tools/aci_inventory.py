import requests
import json
import time
#import getpass
import urllib3
#import re
#import ipdb
import pprint

username = 'admin'
password = 'NotMyPassword'
apic = '10.11.11.11'

# Disable SSL Warnings
urllib3.disable_warnings()


def login():
    url = 'https://' + apic + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def get_inventory(session, apic=apic):
    url = 'https://' + apic + '/api/node/mo/topology/pod-1.json?query-target=children&target-subtree-class=fabricNode'
    response = session.get(url, verify=False)
    return response


session = login()
inventory = get_inventory(session=session, apic=apic)
inventory = json.loads(inventory.text)
pprint.pprint(inventory['imdata'])
for node in inventory['imdata']:
    print('ID: ' + node['fabricNode']['attributes']['id'])
    print('Model: ' + node['fabricNode']['attributes']['model'])
    print('Role: ' + node['fabricNode']['attributes']['role'])
    print('Serial: ' + node['fabricNode']['attributes']['serial'])
    print('')
