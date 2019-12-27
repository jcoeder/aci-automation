#d
import requests
import json
import time
import getpass

username = 'admin'
password = 'PASSWORD'
#username = input("APIC Username: ")
#password = getpass.getpass()
apic1 = '172.31.33.201'
leaf_prefix = 'LEAF-'
leaf_start = 100
spine_prefix = 'SPINE-'
spine_start = 200
leaf_list = []
spine_list = []

# Disable SSL Warnings
requests.urllib3.disable_warnings()

def login():
    '''
    Log into APIC and return session
    '''
    url = 'https://' + apic1 + '/api/aaaLogin.json'
    payload = {'aaaUser':{'attributes':{'name':username,'pwd':password}}}
    session = requests.Session()
    response = session.post(url, json=payload, verify=False)
    return session


def find_available_nodes():
    '''
    json_repsonse will look something like this:
{
  "totalCount": "1",
  "imdata": [
    {
      "dhcpClient": {
        "attributes": {
          "capabilities": "multi-pod-bringup",
          "childAction": "",
          "clientEvent": "requesting",
          "configIssues": "",
          "configNodeRole": "unspecified",
          "decomissioned": "no",
          "dn": "client-[TEP-1-101]",
          "extPoolId": "0",
          "fabricId": "1",
          "fwVer": "",
          "hwAddr": "00:00:00:00:00:00",
          "id": "TEP-1-101",
          "ip": "0.0.0.0",
          "lcOwn": "local",
          "modTs": "2019-12-27T19:30:21.162+00:00",
          "model": "N9K-C9396PX",
          "name": "",
          "nameAlias": "",
          "nodeId": "0",
          "nodeRole": "leaf",
          "nodeType": "unspecified",
          "podId": "1",
          "relayIp": "0.0.0.0",
          "runningVer": "",
          "spineLevel": "0",
          "status": "",
          "supported": "yes"
        }
      }
    }
  ]
}
    '''
    url = 'https://' + apic1 + '/api/node/class/dhcpClient.json?query-target-filter=and(not(wcard(dhcpClient.dn,"__ui_")),and(or(eq(dhcpClient.ip,"0.0.0.0")),or(eq(dhcpClient.nodeRole,"spine"),eq(dhcpClient.nodeRole,"leaf"),eq(dhcpClient.nodeRole,"unsupported"))))'
    response = session.get(url, verify=False)
    response = json.loads(response.text)
    json_response = json.dumps(response, indent=2)
    return response


def find_existing_nodes():
    '''
    '''
    url = 'https://' + apic1 + '/api/node/class/dhcpClient.json?query-target-filter=and(not(wcard(dhcpClient.dn,"__ui_")),and(and(ne(dhcpClient.nodeId,"0"),ne(dhcpClient.ip,"0.0.0.0")),or(eq(dhcpClient.nodeRole,"spine"),eq(dhcpClient.nodeRole,"leaf"))))'
    response = session.get(url, verify=False)
    response = json.loads(response.text)
    json_response = json.dumps(response, indent=2)
    global leaf_list
    global spine_list
    for item in response['imdata']:
        if item['dhcpClient']['attributes']['nodeRole'] == 'leaf':
            leaf_list.append(int(item['dhcpClient']['attributes']['nodeId']))
        elif item['dhcpClient']['attributes']['nodeRole'] == 'spine':
            spine_list.append(int(item['dhcpClient']['attributes']['nodeId']))


def add_nodes():
    '''
    '''
    url = 'https://' + apic1 + '/api/node/mo/uni/controller/nodeidentpol.json'
    while True:
        time.sleep(5)
        nodes = find_available_nodes()
        find_existing_nodes()
        if nodes['totalCount'] == '0':
            time.sleep(5)
        elif nodes['totalCount'] == '1':
            if nodes['imdata'][0]['dhcpClient']['attributes']['nodeRole'] == "leaf":
                if leaf_list == []:
                    global leaf_start
                    leaf_start += 1
                    leaf_start_str = str(leaf_start)
                    nodeid = leaf_start_str
                    name = leaf_prefix + leaf_start_str
                    identifier = nodes['imdata'][0]['dhcpClient']['attributes']['id']
                    payload = {"fabricNodeIdentP":{"attributes":{"dn":"uni/controller/nodeidentpol/nodep-" + identifier,"nodeId":nodeid,"name":name,"status":"created,modified"},"children":[]}}
                    response = session.post(url, json=payload, verify=False)
                else:
                    max_leaf = int(max(leaf_list))
                    nodeid = max_leaf + 1
                    nodeid = str(nodeid)
                    name = leaf_prefix + nodeid
                    identifier = nodes['imdata'][0]['dhcpClient']['attributes']['id']
                    payload = {"fabricNodeIdentP":{"attributes":{"dn":"uni/controller/nodeidentpol/nodep-" + identifier,"nodeId":nodeid,"name":name,"status":"created,modified"},"children":[]}}
                    response = session.post(url, json=payload, verify=False)                	
            elif nodes['imdata'][0]['dhcpClient']['attributes']['nodeRole'] == "spine":
                if spine_list == []:
                    global spine_start
                    spine_start += 1
                    spine_start_str = str(spine_start)
                    nodeid = spine_start_str
                    name = spine_prefix + spine_start_str
                    identifier = nodes['imdata'][0]['dhcpClient']['attributes']['id']
                    payload = {"fabricNodeIdentP":{"attributes":{"dn":"uni/controller/nodeidentpol/nodep-" + identifier,"nodeId":nodeid,"name":name,"status":"created,modified"},"children":[]}}
                    response = session.post(url, json=payload, verify=False)
                else:
                    max_spine = int(max(spine_list))
                    nodeid = max_spine + 1
                    nodeid = str(nodeid)
                    name = spine_prefix + nodeid
                    identifier = nodes['imdata'][0]['dhcpClient']['attributes']['id']
                    payload = {"fabricNodeIdentP":{"attributes":{"dn":"uni/controller/nodeidentpol/nodep-" + identifier,"nodeId":nodeid,"name":name,"status":"created,modified"},"children":[]}}
                    response = session.post(url, json=payload, verify=False)
            elif nodes['imdata'][0]['dhcpClient']['attributes']['nodeRole'] == "apic":
            	exit()
            else:
                exit()
        elif int(nodes['totalCount']) >= 2:
        	exit()
        else:
        	exit()


session = login()
add_nodes()
