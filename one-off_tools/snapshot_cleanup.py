import requests
import json
import time
#import getpass
import urllib3
import ipdb
import pprint

username = 'admin'
password = 'NotMyPassword'
apic = '172.31.16.5'
proto = 'https://'
preamble = proto + apic


# Disable SSL Warnings
urllib3.disable_warnings()


def login():
	# Log into APIC and create a requests Session that can be reused.
    url = preamble + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def get_snapshots(session):
    url = preamble + '/api/node/class/configSnapshot.json'
    response = session.get(url, verify=False)
    #pprint.pprint(response.text)
    snapshots = json.loads(response.text)
    snapshots = snapshots['imdata']
    return snapshots


def delete_snapshots(session, snapshots, pattern):
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/backupst/snapshots-[uni/fabric/configexp-defaultOneTime]/snapshot-run-2021-05-02T19-38-52.json
    #payload{"configSnapshot":{"attributes":{"dn":"uni/backupst/snapshots-[uni/fabric/configexp-defaultOneTime]/snapshot-run-2021-05-02T19-38-52","retire":"true"},"children":[]}}
    for snapshot in snapshots:
        if pattern in snapshot['configSnapshot']['attributes']['descr']:
            dn = snapshot['configSnapshot']['attributes']['dn']
            url  = preamble + '/api/node/mo/' + dn + '.json'
            payload_string = '{"configSnapshot":{"attributes":{"dn":"' + dn + '","retire":"true"},"children":[]}}'
            payload = json.loads(payload_string)
            print(session.post(url, json=payload, verify=False))
        else:
        	pass



if __name__ == "__main__":
    session = login()
    snapshots = get_snapshots(session=session)
    delete_snapshots(session=session, snapshots=snapshots, pattern='')
