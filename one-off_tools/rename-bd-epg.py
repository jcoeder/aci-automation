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
tenant = 'HOME_LAB_TENANT'
application_profile = 'PROD_AP'
old_bridge_domain = ''
new_bridge_domain = ''
old_epg = ''
new_epg = ''

# Disable SSL Warnings
urllib3.disable_warnings()


def login():
	# Log into APIC and create a requests Session that can be reused.
    url = preamble + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def create_snapshot(session, apic, old_bridge_domain, old_epg):
	# Create a snapshot of the configuration so it can be rolled back if needed.
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/fabric/configexp-defaultOneTime.json
    #{"configExportP":{"attributes":{"dn":"uni/fabric/configexp-defaultOneTime","name":"defaultOneTime","snapshot":"true","targetDn":"","adminSt":"triggered","rn":"configexp-defaultOneTime","status":"created,modified","descr":"YAHOO"},"children":[]}}
    #payload"{\"configExportP\":{\"attributes\":{\"dn\":\"uni/fabric/configexp-defaultOneTime\",\"name\":\"defaultOneTime\",\"snapshot\":\"true\",\"targetDn\":\"\",\"adminSt\":\"triggered\",\"rn\":\"configexp-defaultOneTime\",\"status\":\"created,modified\",\"descr\":\"THIS IS A TEST\"},\"children\":[]}}"
    #response: {"totalCount":"0","imdata":[]}
    snapshot_description = '"RENAME ' + old_bridge_domain + ' AND ' + old_epg + '"'
    payload_string = '{"configExportP":{"attributes":{"dn":"uni/fabric/configexp-defaultOneTime","adminSt":"triggered","descr":' + snapshot_description + '}}}'
    url = preamble + '/api/mo.json'
    payload = json.loads(payload_string)
    response = session.post(url, json=payload, verify=False)
    print('Created snapshot with description: ' + snapshot_description)


def get_epgs(session, apic):
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '.json?query-target=children&target-subtree-class=fvAEPg&rsp-subtree=full&rsp-prop-include=config-only'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def get_bds(session, apic):
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '.json?query-target=children&target-subtree-class=fvBD&rsp-subtree=full&rsp-prop-include=config-only'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def delete_old_bd(session, apic, tenant, old_bridge_domain):
    #https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/BD-VLAN_10_BD.json
    #{"fvBD":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/BD-VLAN_10_BD","status":"deleted"},"children":[]}}
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/BD-VLAN_20_BD.json
    #payload{"fvBD":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/BD-VLAN_20_BD","status":"deleted"},"children":[]}}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/BD-' + old_bridge_domain + '.json'
    payload_string = '{"fvBD":{"attributes":{"dn":"uni/tn-' + tenant + '/BD-' + old_bridge_domain + '","status":"deleted"}}}'
    payload = json.loads(payload_string)
    response = session.post(url, json=payload, verify=False)
    print('Deleting old bridge domain: ' + old_bridge_domain)


def delete_old_epg(session, apic, tenant, application_profile, old_epg):
    #https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/ap-PROD_AP/epg-VLAN_10_EPG.json
    #{"fvAEPg":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/ap-PROD_AP/epg-VLAN_10_EPG","status":"deleted"},"children":[]}}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '/epg-' + old_epg + '.json'
    payload_string = '{"fvAEPg":{"attributes":{"dn":"uni/tn-' + tenant + '/ap-' + application_profile + '/epg-' + old_epg + '","status":"deleted"},"children":[]}}'
    payload = json.loads(payload_string)
    response = session.post(url, json=payload, verify=False)
    print('Deleting old epg: ' + old_bridge_domain)


def recreate_new_bd(session, apic, tenant, bds, old_bridge_domain, new_bridge_domain):
    # Create BD
    #https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/BD-EXAMPLE.json
    #{"fvBD":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/BD-EXAMPLE","mac":"00:22:BD:F8:19:FF","arpFlood":"true","name":"EXAMPLE","nameAlias":"EXAMPLE","descr":"EXAMPLE","rn":"BD-EXAMPLE","status":"created"},"children":[{"fvSubnet":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/BD-EXAMPLE/subnet-[192.168.255.1/24]","ctrl":"","ip":"192.168.255.1/24","scope":"public","descr":"EXAMPLE","rn":"subnet-[192.168.255.1/24]","status":"created"},"children":[]}},{"fvRsCtx":{"attributes":{"tnFvCtxName":"HOME_LAB_VRF","status":"created,modified"},"children":[]}}]}}
    #pprint.pprint(bds)
    for bd in bds['imdata']:
        if bd['fvBD']['attributes']['name'] == old_bridge_domain:
            old_bridge_domain_json = bd
    old_bridge_domain_json_string = json.dumps(old_bridge_domain_json, separators=(',',':'))
    new_bridge_domain_json_string = old_bridge_domain_json_string.replace(old_bridge_domain, new_bridge_domain)
    payload = json.loads(new_bridge_domain_json_string)
    url = preamble + '/api/node/mo/uni/tn-' + tenant +'/BD-' + new_bridge_domain + '.json'
    response = session.post(url, json=payload, verify=False)
    #print(response.text)
    print('Recreating new bridge domain: ' + new_bridge_domain)
    for child in old_bridge_domain_json['fvBD']['children']:
        if 'fvSubnet' in child:
            print('Subnet: ' + child['fvSubnet']['attributes']['ip'])


def recreate_new_epg(session, apic, tenant, application_profile, epgs, old_epg, new_epg, old_bridge_domain, new_bridge_domain):
    # Create EPG
    #https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/ap-PROD_AP/epg-EXAMPLE.json
    #{"fvAEPg":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/ap-PROD_AP/epg-EXAMPLE","prio":"level3","name":"EXAMPLE","nameAlias":"EXAMPLE","descr":"EXAMPLE","rn":"epg-EXAMPLE","status":"created"},"children":[{"fvRsBd":{"attributes":{"tnFvBDName":"EXAMPLE","status":"created,modified"},"children":[]}}]}}
    #pprint.pprint(epgs)
    for epg in epgs['imdata']:
        if epg['fvAEPg']['attributes']['name'] == old_epg:
            old_epg_json = epg
    old_epg_json_string = json.dumps(old_epg_json, separators=(',',':'))
    new_epg_json_string = old_epg_json_string.replace(old_epg, new_epg)
    new_epg_json_string = new_epg_json_string.replace(old_bridge_domain, new_bridge_domain)
    payload = json.loads(new_epg_json_string)
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '/epg-' + new_epg +'.json'
    response = session.post(url, json=payload, verify=False)
    print('Recreating new EPG: ' + new_epg)


def does_epg_reference_bd(bds, epgs, old_bridge_domain, old_epg):
    # Check old EPG references old BD
    for epg in epgs['imdata']:
        if epg['fvAEPg']['attributes']['name'] == old_epg:
            filtered_old_epg = epg
            break
        else:
            filtered_old_epg = None

    for children in filtered_old_epg['fvAEPg']['children']:
    	# Try because not different children have different keys
        try:
        	# Do not increment children_index if found
            if children['fvRsBd']['attributes']['tnFvBDName'] == old_bridge_domain:
                print('Bridge domain found in EPG configuration.. Continuing..')
                continue
            # Exit out of program if bridge domain not found in EPG
            else:
                print('Bridge domain not found in EPG configuration.  Check provided EPG and BD name.')
                exit()
        # If there is a key error this is not the bridge domain children we are looking for
        # continue to next children in list
        except KeyError:
            continue


def old_bd_in_old_epg(epgs, old_epg):
    #pprint.pprint(epgs)
    for epg in epgs['imdata']:
        if epg['fvAEPg']['attributes']['name'] == old_epg:
            for child in epg['fvAEPg']['children']:
                #pprint.pprint(child)
                if 'fvRsBd' in child:
                    old_bridge_domain = child['fvRsBd']['attributes']['tnFvBDName']
                else:
                    pass
        else:
            pass
    print('Old Bridge Domain: ' + old_bridge_domain)
    return old_bridge_domain


def get_old_bd(bd_list):
    # Validate provided old BD is an existing BD
    while True:
        old_bridge_domain = input('Old Bridge Domain: ')
        if old_bridge_domain not in bd_list:
            print('Not a valid BD.  Please select from list without quotes.')
            print('BDs: ' + str(bd_list))
        elif old_bridge_domain in bd_list:
            return old_bridge_domain


def get_old_epg(epg_list):
    # Validate provided old EPG is an existing EPG
    while True:
        old_epg = input('Old EPG: ')
        if old_epg not in epg_list:
            print('Not a valid EPG.  Please select from list without quotes.')
            print('EPGs: ' + str(epg_list))
        elif old_epg in old_epg:
            return old_epg


def validate_new_bd():
    # Make sure a non empty string is provided
    while True:
        new_bridge_domain = input('New Bridge Domain: ')
        if new_bridge_domain == '':
            print('Please provide a valid BD name.')
        else:
            break
    return new_bridge_domain


def validate_new_epg():
    # Make sure a non empty string is provided
    while True:
        new_epg = input('New EPG: ')
        if new_epg == '':
            print('Please provide a valid EPG name.')
        else:
            break
    return new_epg


def list_epgs(epgs):
    epg_list = []
    for epg in epgs['imdata']:
    #    pprint.pprint(json.dumps(epg, separators=(',',':')))
    #    pprint.pprint(epg)
        epg_list.append(epg['fvAEPg']['attributes']['name'])
    print('EPGs: ' + str(epg_list))
    return epg_list


def list_bds(bds):
    bd_list = []
    for bd in bds['imdata']:
    #    print(json.dumps(bd, separators=(',',':')))
    #    pprint.pprint(bd)
        bd_list.append(bd['fvBD']['attributes']['name'])
    print('BDs: ' + str(bd_list))
    return bd_list


if __name__ == "__main__":
	# Log in and create session
    session=login()

    # Get and list all BDs.  Save JSON output as bds
    bds = get_bds(session=session, apic=apic)
    #bd_list = list_bds(bds=bds)

    # Get and list all EPGs.  Save JSON output as epgs
    epgs = get_epgs(session=session, apic=apic)
    epg_list = list_epgs(epgs=epgs)

    # Get old bridge domain from user
    #old_bridge_domain = get_old_bd(bd_list=bd_list)

    # Get old epg from user
    old_epg = get_old_epg(epg_list=epg_list)

    # Pull old BD from old EPG config
    old_bridge_domain = old_bd_in_old_epg(epgs=epgs, old_epg=old_epg)

    # Get new EPG from user and make sure new EPG is not en empty string
    new_epg = validate_new_epg()

    # Get new BD from user and make sure new BD is not an empty string
    new_bridge_domain = validate_new_bd()

    # Check old EPG references old BD
    # Used before extracting BD from EPG configuration, no longer needed.
    #does_epg_reference_bd(bds=bds, epgs=epgs, old_bridge_domain=old_bridge_domain, old_epg=old_epg)

    # Create a snapshot of the configuration.
    create_snapshot(session=session, apic=apic, old_bridge_domain=old_bridge_domain, old_epg=old_epg)

    # Delete old bridge domain
    delete_old_bd(session=session, apic=apic, tenant=tenant, old_bridge_domain=old_bridge_domain)

    # Delete old epg
    delete_old_epg(session=session, apic=apic, tenant=tenant, application_profile=application_profile, old_epg=old_epg)

    # Recreate new bridge domain
    recreate_new_bd(session=session, apic=apic, tenant=tenant, bds=bds, old_bridge_domain=old_bridge_domain, new_bridge_domain=new_bridge_domain)

    # Recreate new epg
    recreate_new_epg(session=session, apic=apic, tenant=tenant, application_profile=application_profile, epgs=epgs, old_epg=old_epg, new_epg=new_epg, old_bridge_domain=old_bridge_domain, new_bridge_domain=new_bridge_domain)

