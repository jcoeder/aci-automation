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


#/api/node/class/polUni.json?&order-by=polUni.modTs|desc

def login():
	# Log into APIC and create a requests Session that can be reused.
    url = preamble + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def get_root(session, apic):
    url = preamble + '/api/class/uni.json'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def get_infra_config(session, apic):
    url = preamble + '/api/node/mo/uni/infra.json?query-target=self&rsp-subtree=full&rsp-prop-include=config-only'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def apply_infra_config(session, apic, infra_config):
    url = preamble + '/api/node/mo/uni/infra.json'
    payload = infra_config
    response = session.post(url, json=payload, verify=False)
    print(response.text)


def get_ap(session, apic):
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '.json?query-target=self&rsp-subtree=full&rsp-prop-include=config-only'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def delete_ap(session, apic, tenant, application_profile):
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/ap-PROD_AP.json
    #payload{"fvAp":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/ap-PROD_AP","status":"deleted"},"children":[]}}
    #response: {"totalCount":"0","imdata":[]}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '.json'
    payload_string = '{"fvAp":{"attributes":{"dn":"uni/tn-' + tenant + '/ap-' + application_profile + '","status":"deleted"}}}'
    payload = json.loads(payload_string)
    response = session.post(url, json=payload, verify=False)
    print('Deleting old application profile: ' + application_profile)


def create_ap(session, apic, tenant, application_profile, ap_json):
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/tn-HOME_LAB_TENANT/ap-TESINGABC.json
    #payload{"fvAp":{"attributes":{"dn":"uni/tn-HOME_LAB_TENANT/ap-TESINGABC","name":"TESINGABC","nameAlias":"TESINGABC","descr":"TESINGABC","rn":"ap-TESINGABC","status":"created"},"children":[]}}
    #response: {"totalCount":"0","imdata":[]}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '/ap-' + application_profile + '.json'
    payload = ap_json
    response = session.post(url, json=payload, verify=False)
    print(response.text)


def get_tenant(session, apic):
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '.json?query-target=self&rsp-subtree=full'
    response = session.get(url, verify=False)
    return json.loads(response.text)


def delete_tenant(session, apic, tenant):
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/tn-TESTING123.json
    #payload{"fvTenant":{"attributes":{"dn":"uni/tn-TESTING123","status":"deleted"},"children":[]}}
    #response: {"totalCount":"0","imdata":[]}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '.json'
    payload_string = '{"fvTenant":{"attributes":{"dn":"uni/tn-' + tenant + '","status":"deleted"}}}'
    payload = json.loads(payload_string)
    response = session.post(url, json=payload, verify=False)
    print('Deleting old Tenant: ' + tenant)


def create_tenant(session, apic, tenant, tenant_json):
    #method: POST
    #url: https://172.31.16.5/api/node/mo/uni/tn-TESTING123.json
    #payload{"fvTenant":{"attributes":{"dn":"uni/tn-TESTING123","name":"TESTING123","nameAlias":"TESTING123","descr":"TESTING123","rn":"tn-TESTING123","status":"created"},"children":[{"fvCtx":{"attributes":{"dn":"uni/tn-TESTING123/ctx-TESTING123","name":"TESTING123","rn":"ctx-TESTING123","status":"created"},"children":[]}}]}}
    #response: {"totalCount":"0","imdata":[]}
    url = preamble + '/api/node/mo/uni/tn-' + tenant + '.json'
    payload = tenant_json
    response = session.post(url, json=payload, verify=False)
    print(response.text)


if __name__ == "__main__":
    # Log in and create session
    session=login()
    root = get_root(session, apic)
    print(root)
    #infra_config = get_infra_config(session=session, apic=apic)
    #print(infra_config)
    #ipdb.set_trace()
    #apply_infra_config(session=session, apic=apic, infra_config=infra_config)
    #ap_json = get_ap(session=session, apic=apic)
    #ap_json = ap_json['imdata'][0]
    #print(ap_json)
    #tenant_json = get_tenant(session=session, apic=apic)
    #tenant_json = tenant_json['imdata'][0]
    #print(tenant_json)
    #delete_tenant(session=session, apic=apic, tenant=tenant)
    #create_tenant(session=session, apic=apic, tenant=tenant, tenant_json=tenant_json)
    #delete_ap(session=session, apic=apic, tenant=tenant, application_profile=application_profile)
    #create_ap(session=session, apic=apic, tenant=tenant, application_profile=application_profile, ap_json=ap_json)
