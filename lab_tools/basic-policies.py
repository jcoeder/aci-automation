import requests
import json
import time
import getpass
import urllib3

username = 'admin'
password = 'PASSWORD'
#username = input("APIC Username: ")
password = getpass.getpass()
apic1 = '172.31.33.50'

# Disable SSL Warnings
urllib3.disable_warnings()

def login():
    '''
    Log into APIC and return session
    '''
    url = 'https://' + apic1 + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def create_tenant(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF'):
    '''
    Create ACI Tenant
    '''
    url = 'https://' + apic + '/api/node/mo/uni/tn-' + tenant_name + '.json'
    json = {'fvTenant':{'attributes':{'dn':'uni/tn-' + tenant_name,'name':tenant_name,'rn':'tn-' + tenant_name,'status':'created'},'children':[{'fvCtx':{'attributes':{'dn':'uni/tn-' + tenant_name + '/ctx-' + vrf_name,'name':vrf_name,'rn':'ctx-' + vrf_name,'status':'created'},'children':[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_static_all_vlans_vlan_pool(session, apic=apic1, pool_name='ALL_VLANS_VLP'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/vlanns-[' + pool_name + ']-static.json'
    json = {"fvnsVlanInstP":{"attributes":{"dn":"uni/infra/vlanns-[" + pool_name + "]-static","name":pool_name,"allocMode":"static","descr":pool_name,"rn":"vlanns-[" + pool_name + "]-static","status":"created"},"children":[{"fvnsEncapBlk":{"attributes":{"dn":"uni/infra/vlanns-[" + pool_name + "]-static/from-[vlan-1]-to-[vlan-4094]","from":"vlan-1","to":"vlan-4094","allocMode":"static","rn":"from-[vlan-1]-to-[vlan-4094]","status":"created"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_default_aep(session, apic=apic1, aep_name='DEFAULT_AEP'):
    url = 'https://' + apic + '/api/node/mo/uni/infra.json'
    json = {"infraInfra":{"attributes":{"dn":"uni/infra","status":"modified"},"children":[{"infraAttEntityP":{"attributes":{"dn":"uni/infra/attentp-" + aep_name,"name":aep_name,"descr":aep_name,"rn":"attentp-" + aep_name,"status":"created"},"children":[]}},{"infraFuncP":{"attributes":{"dn":"uni/infra/funcprof","status":"modified"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_phys_domain(session, apic=apic1, domain_name='ALL_VLANS_PHY', pool_name='ALL_VLANS_VLP'):
    url = 'https://' + apic + '/api/node/mo/uni/phys-' + domain_name + '.json'
    json = {"physDomP":{"attributes":{"dn":"uni/phys-" + domain_name,"name":domain_name,"rn":"phys-" + domain_name,"status":"created"},"children":[{"infraRsVlanNs":{"attributes":{"tDn":"uni/infra/vlanns-[" + pool_name + "]-static","status":"created"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def aep_to_domain(session, apic=apic1, domain_name='ALL_VLANS_PHY', aep_name='DEFAULT_AEP'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/attentp-' + aep_name + '.json'
    json = {"infraRsDomP":{"attributes":{"tDn":"uni/phys-" + domain_name,"status":"created,modified"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_network_centric_epg(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF', ap_name = 'JUSTIN_AP', bd_name='VLAN10_BD', epg_name='VLAN10_EPG', subnet='10.10.10.1/24', domain_name='ALL_VLANS_PHYS'):
    '''
    '''
    url = 'https://' + apic + '/api/node/mo/uni/tn-' + tenant_name + '/BD-' + bd_name + '.json'
    json = {"fvBD":{"attributes":{"dn":"uni/tn-" + tenant_name + "/BD-" + bd_name,"mac":"00:22:BD:F8:19:FF","arpFlood":"true","name":bd_name,"nameAlias":bd_name,"descr":bd_name,"rn":"BD-" + bd_name,"status":"created"},"children":[{"fvSubnet":{"attributes":{"dn":"uni/tn-" + tenant_name + "/BD-" + bd_name + "/subnet-[" + subnet + "]","ctrl":"","ip":subnet,"scope":"public","rn":"subnet-[" + subnet + "]","status":"created"},"children":[]}},{"fvRsCtx":{"attributes":{"tnFvCtxName":vrf_name,"status":"created,modified"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)

    url = 'https://' + apic + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + ap_name + '.json'
    json = {"fvAp":{"attributes":{"dn":"uni/tn-" + tenant_name + "/ap-" + ap_name,"name":ap_name,"nameAlias":ap_name,"descr":ap_name,"rn":"ap-" + ap_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)

    url = 'https://' + apic + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + ap_name + '/epg-' + epg_name + '.json'
    json = {"fvAEPg":{"attributes":{"dn":"uni/tn-" + tenant_name + "/ap-" + ap_name + "/epg-" + epg_name,"name":epg_name,"nameAlias":epg_name,"descr":epg_name,"prefGrMemb":"include","rn":"epg-" + epg_name,"status":"created"},"children":[{"fvRsBd":{"attributes":{"tnFvBDName":bd_name,"status":"created,modified"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)

    url = 'https://' + apic + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + ap_name + '/epg-' + epg_name + '.json'
    json = {"fvRsDomAtt":{"attributes":{"resImedcy":"immediate","tDn":"uni/phys-" + domain_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_link_auto_policy(session, apic=apic1, policy_name='LINK_LEVEL_AUTO_INTPOL'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/hintfpol-' + policy_name + '.json'
    json = {"fabricHIfPol":{"attributes":{"dn":"uni/infra/hintfpol-" + policy_name,"name":policy_name,"descr":policy_name,"rn":"hintfpol-" + policy_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_cdp_policy(session, apic=apic1, policy_name='CDP_ENABLED_INTPOL', state='enabled'):
    '''
    Create CDP policies
    '''
    url = 'https://' + apic + '/api/node/mo/uni/infra/cdpIfP-' + policy_name + '.json'
    json = {"cdpIfPol":{"attributes":{"dn":"uni/infra/cdpIfP-" + policy_name,"adminSt":state,"name":policy_name,"descr":policy_name,"rn":"cdpIfP-" + policy_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_lldp_policy(session, apic=apic1, policy_name='LLDP_ENABLED_INTPOL', state='enabled'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/lldpIfP-' + policy_name + '.json'
    json = {"lldpIfPol":{"attributes":{"dn":"uni/infra/lldpIfP-" + policy_name,"adminRxSt":state,"adminTxSt":state},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_pc_policy(session, apic=apic1, policy_name='PC_ACTIVE_INTPOL', mode='active'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/lacplagp-' + policy_name + '.json'
    json = {"lacpLagPol":{"attributes":{"dn":"uni/infra/lacplagp-" + policy_name,"name":policy_name,"descr":policy_name,"mode":mode,"rn":"lacplagp-" + policy_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_mcp_policy(session, apic=apic1, policy_name='MCP_ENABLED_INTPOL', state='enabled'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/mcpIfP-' + policy_name + '.json'
    json = {"mcpIfPol":{"attributes":{"dn":"uni/infra/mcpIfP-" + policy_name,"name":policy_name,"descr":policy_name,"adminSt":state,"rn":"mcpIfP-" + policy_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_storm_control_policy(session, apic=apic1, policy_name='STORM_CONTROL_50_DROP_INTPOL', percent='50', action='drop'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/stormctrlifp-' + policy_name + '.json'
    json = {"stormctrlIfPol":{"attributes":{"dn":"uni/infra/stormctrlifp-" + policy_name,"name":policy_name,"descr":policy_name,"rate":percent,"burstRate":percent,"rn":"stormctrlifp-" + policy_name,"status":"created"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_interface_policy_group(session, apic=apic1, policy_name='DEFAULT_LEAF_ACCESS_IPG'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/funcprof/accportgrp-' + policy_name + '.json'
    json = {"infraAccPortGrp":{"attributes":{"dn":"uni/infra/funcprof/accportgrp-" + policy_name,"name":policy_name,"descr":policy_name,"rn":"accportgrp-" + policy_name,"status":"created"},"children":[{"infraRsHIfPol":{"attributes":{"tnFabricHIfPolName":"LINK_LEVEL_AUTO_INTPOL","status":"created,modified"},"children":[]}},{"infraRsCdpIfPol":{"attributes":{"tnCdpIfPolName":"CDP_ENABLED_INTPOL","status":"created,modified"},"children":[]}},{"infraRsAttEntP":{"attributes":{"tDn":"uni/infra/attentp-DEFAULT_AEP","status":"created,modified"},"children":[]}},{"infraRsMcpIfPol":{"attributes":{"tnMcpIfPolName":"MCP_ENABLED_INTPOL","status":"created,modified"},"children":[]}},{"infraRsLldpIfPol":{"attributes":{"tnLldpIfPolName":"LLDP_ENABLED_INTPOL","status":"created,modified"},"children":[]}},{"infraRsStormctrlIfPol":{"attributes":{"tnStormctrlIfPolName":"STORM_CONTROL_50_DROP_INTPOL","status":"created,modified"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_leaf_access_policy_group(session, apic=apic1, policy_name='DEFAULT_LEAF_SPG'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/funcprof/accnodepgrp-' + policy_name + '.json'
    json = {"infraAccNodePGrp":{"attributes":{"dn":"uni/infra/funcprof/accnodepgrp-" + policy_name,"name":policy_name,"descr":policy_name,"rn":"accnodepgrp-" + policy_name,"status":"created"},"children":[{"infraRsLeafPGrpToCdpIfPol":{"attributes":{"tnCdpIfPolName":"CDP_ENABLED_INTPOL","status":"created,modified"},"children":[]}},{"infraRsLeafPGrpToLldpIfPol":{"attributes":{"tnLldpIfPolName":"LLDP_ENABLED_INTPOL","status":"created,modified"},"children":[]}}]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)  


def create_leaf_profile(session, apic=apic1, policy_name='', node_from='101', node_to='101'):
    url = 'https://' + apic + '/api/node/mo/uni/infra/nprof-' + policy_name + '.json'
    json = {"infraNodeP":{"attributes":{"dn":"uni/infra/nprof-" + policy_name,"name":policy_name,"descr":policy_name,"rn":"nprof-" + policy_name,"status":"created,modified"},"children":[{"infraLeafS":{"attributes":{"dn":"uni/infra/nprof-" + policy_name + "/leaves-" + policy_name + "-typ-range","type":"range","name":policy_name,"rn":"leaves-" + policy_name + "-typ-range","status":"created"},"children":[{"infraNodeBlk":{"attributes":{"dn":"uni/infra/nprof-" + policy_name + "/leaves-" + policy_name +"-typ-range/nodeblk-493d8dfac177bafd","from_":node_from,"to_":node_to,"name":"493d8dfac177bafd","rn":"nodeblk-493d8dfac177bafd","status":"created"},"children":[]}},{"infraRsAccNodePGrp":{"attributes":{"tDn":"uni/infra/funcprof/accnodepgrp-DEFAULT_LEAF_SPG","status":"created"},"children":[]}}]}}]}}    
    response = session.post(url, json=json, verify=False)
    print(response.text)


def create_interface_profile(session, apic=apic1, policy_name=''):
    url = 'https://' + apic + '/api/node/mo/uni/infra/accportprof-' + policy_name + '.json'
    json = {"infraAccPortP":{"attributes":{"dn":"uni/infra/accportprof-" + policy_name,"name":policy_name,"descr":policy_name,"rn":"accportprof-" + policy_name,"status":"created,modified"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


def leaf_to_interface_profile(session, apic=apic1, policy_name=''):
    url = 'https://' + apic + '/api/node/mo/uni/infra/nprof-' + policy_name + '.json'
    json = {"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-" + policy_name,"status":"created,modified"},"children":[]}}
    response = session.post(url, json=json, verify=False)
    print(response.text)


session = login()

# Interface Policies
create_link_auto_policy(session, apic=apic1, policy_name='LINK_LEVEL_AUTO_INTPOL')
create_pc_policy(session, apic=apic1, policy_name='PC_ACTIVE_INTPOL', mode='active')
create_cdp_policy(session, apic=apic1, policy_name='CDP_ENABLED_INTPOL', state='enabled')
create_cdp_policy(session, apic=apic1, policy_name='CDP_DISABLED_INTPOL', state='disabled')
create_lldp_policy(session, apic=apic1, policy_name='LLDP_ENABLED_INTPOL', state='enabled')
create_lldp_policy(session, apic=apic1, policy_name='LLDP_DISABLED_INTPOL', state='disabled')
create_mcp_policy(session, apic=apic1, policy_name='MCP_ENABLED_INTPOL', state='enabled')
create_mcp_policy(session, apic=apic1, policy_name='MCP_DISABLED_INTPOL', state='disabled')
create_storm_control_policy(session, apic=apic1, policy_name='STORM_CONTROL_50_DROP_INTPOL', percent='50', action='drop')
create_interface_policy_group(session, apic=apic1, policy_name='DEFAULT_LEAF_ACCESS_IPG')

# Leaf Profiles
create_leaf_access_policy_group(session, apic=apic1, policy_name='DEFAULT_LEAF_SPG')
create_leaf_profile(session, apic=apic1, policy_name='LEAF_101', node_from='101', node_to='101')
create_leaf_profile(session, apic=apic1, policy_name='LEAF_102', node_from='102', node_to='102')
create_leaf_profile(session, apic=apic1, policy_name='LEAF_101_102', node_from='101', node_to='102')
create_interface_profile(session, apic=apic1, policy_name='LEAF_101')
create_interface_profile(session, apic=apic1, policy_name='LEAF_102')
create_interface_profile(session, apic=apic1, policy_name='LEAF_101_102')
leaf_to_interface_profile(session, apic=apic1, policy_name='LEAF_101')
leaf_to_interface_profile(session, apic=apic1, policy_name='LEAF_102')
leaf_to_interface_profile(session, apic=apic1, policy_name='LEAF_101_102')

# AEP, VLAN Pool, Physical Domain
create_static_all_vlans_vlan_pool(session, apic=apic1, pool_name='ALL_VLANS_VLP')
create_default_aep(session, apic=apic1, aep_name='DEFAULT_AEP')
create_phys_domain(session, apic=apic1, domain_name='ALL_VLANS_PHY', pool_name='ALL_VLANS_VLP')
aep_to_domain(session, apic=apic1, domain_name='ALL_VLANS_PHY', aep_name='DEFAULT_AEP')

# Tenant, Bridge Domains, Endpoint Groups
create_tenant(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF')
create_network_centric_epg(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF', ap_name='JUSTIN_AP', bd_name='VLAN10_BD', epg_name='VLAN10_EPG', subnet='10.10.10.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF', ap_name='JUSTIN_AP', bd_name='VLAN20_BD', epg_name='VLAN20_EPG', subnet='10.10.20.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='JUSTIN_TN', vrf_name='JUSTIN_VRF', ap_name='JUSTIN_AP', bd_name='VLAN30_BD', epg_name='VLAN30_EPG', subnet='10.10.30.1/24')

create_tenant(session, apic=apic1, tenant_name='ALEX_TN', vrf_name='ALEX_VRF')
create_network_centric_epg(session, apic=apic1, tenant_name='ALEX_TN', vrf_name='ALEX_VRF', ap_name='ALEX_AP', bd_name='VLAN40_BD', epg_name='VLAN40_EPG', subnet='10.10.40.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='ALEX_TN', vrf_name='ALEX_VRF', ap_name='ALEX_AP', bd_name='VLAN50_BD', epg_name='VLAN50_EPG', subnet='10.10.50.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='ALEX_TN', vrf_name='ALEX_VRF', ap_name='ALEX_AP', bd_name='VLAN60_BD', epg_name='VLAN60_EPG', subnet='10.10.60.1/24')

create_tenant(session, apic=apic1, tenant_name='AMANDA_TN', vrf_name='AMANDA_VRF')
create_network_centric_epg(session, apic=apic1, tenant_name='AMANDA_TN', vrf_name='AMANDA_VRF', ap_name='AMANDA_AP', bd_name='VLAN70_BD', epg_name='VLAN70_EPG', subnet='10.10.70.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='AMANDA_TN', vrf_name='AMANDA_VRF', ap_name='AMANDA_AP', bd_name='VLAN80_BD', epg_name='VLAN80_EPG', subnet='10.10.80.1/24')
create_network_centric_epg(session, apic=apic1, tenant_name='AMANDA_TN', vrf_name='AMANDA_VRF', ap_name='AMANDA_AP', bd_name='VLAN90_BD', epg_name='VLAN90_EPG', subnet='10.10.90.1/24')
