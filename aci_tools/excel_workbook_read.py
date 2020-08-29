# read in info from the aci workbook

from xl2dict import XlToDict
import yaml
import json

class ACI_Workbook_Read():

    def __init__(self, workbook, ansible_variable_folder):
        # xlsx name is passed in the class creation
        self.workbook = workbook
        self.ansible_variable_folder = ansible_variable_folder
        self.xlobject = XlToDict()
        self.dict_of_sheets = {}

    def read_workbook(self):
        '''
        Read in the ACI workbook and return a dictionary per tab named after the tab
        '''
        # open the aaep_vlan_pool_physical_domain sheet
        aaep_vlan_pool_physical_domain_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="AAEP Domain Pool"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['aaep_vlan_pool_physical_domain_sheet'] = aaep_vlan_pool_physical_domain_sheet
        # we need to pass on the sheet for AAEP/vlan pool/physical domain
        self.aaep_vlan_pool_physical_domain(sheet=aaep_vlan_pool_physical_domain_sheet)

        ### open the interface policy groups sheet
        interface_policy_groups_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Interface Policy Groups"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['interface_policy_groups_sheet'] = interface_policy_groups_sheet
        # we need to pass the sheet for Interface Policy Groups
        self.interface_policy_groups(sheet=interface_policy_groups_sheet)

        ### open the APIC sheet
        apic_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="APIC"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['apic_sheet'] = apic_sheet
        # we need to pass the sheet for APIC
        self.get_apic_ip(sheet=apic_sheet)

        ### open the Fabric Switches sheet
        fabric_switches_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Fabric Switches"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['fabric_switches_sheet'] = fabric_switches_sheet
        # we need to pass the sheet for Fabric Nodes
        self.fabric_nodes(sheet=fabric_switches_sheet)

        ### open the Pod Policies BGP RR sheet
        bgp_route_reflector_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Pod Policy BGP RR"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['bgp_route_reflector_sheet'] = bgp_route_reflector_sheet
        # we need to pass the sheet for the BGP Route Reflectors
        self.bgp_route_reflectors(sheet=bgp_route_reflector_sheet)

        ### open the Leaf Switch Profile Sheet
        leaf_switch_profile_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Leaf Switch Profiles"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['leaf_switch_profile_sheet'] = leaf_switch_profile_sheet
        # we need to pass the sheet for the Switch Profile
        self.leaf_switch_profiles(sheet=leaf_switch_profile_sheet)

        ### open the Spine Switch Profile Sheet
        spine_switch_profile_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Spine Switch Profiles"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['spine_switch_profile_sheet'] = spine_switch_profile_sheet
        # we need to pass the sheet for the Switch Profile
        self.spine_switch_profiles(sheet=spine_switch_profile_sheet)

        ### open the Pod Policies NTP Sheet
        pod_policy_ntp_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Pod Policies NTP"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['pod_policy_ntp_sheet'] = pod_policy_ntp_sheet
        # we need to pass the sheet for the Pod Policies NTP
        self.pod_policy_ntp(sheet=pod_policy_ntp_sheet)

        ### open the Multisite APIC
        multisite_apic_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Multisite APIC"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['multisite_apic_sheet'] = multisite_apic_sheet
        # we need to pass the sheet for the Pod Policies NTP
        self.multisite_apic(sheet=multisite_apic_sheet)

        ### Create ansible inventory for MSO build playbooks
        mso_host_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="MSO Hosts"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_host_sheet'] = mso_host_sheet
        # need to pass the sheet for ansible MSO host inventory to be created
        self.mso_hosts(sheet=mso_host_sheet)

        ### Create MSO tenants variables file
        mso_tenants_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Tenants"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_tenants_sheet'] = mso_tenants_sheet
        # need to pass the sheet for ansible MSO host inventory to be created
        self.mso_tenants(sheet=mso_tenants_sheet)

        ### Create MSO schemas variables file
        mso_schemas_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="MSO Schemas"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_schemas_sheet'] = mso_schemas_sheet
        # need to pass the sheet for ansible MSO host inventory to be created
        self.mso_schemas(sheet=mso_schemas_sheet)

        ### Create MSO filters variables file
        mso_filters_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Filters"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_filters_sheet'] = mso_filters_sheet
        # not going to write a yml file here at this time for mso filters sheet

        ### Create MSO contracts variables file
        mso_contracts_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Contracts"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_contracts_sheet'] = mso_contracts_sheet
        # not going to write a yml file here at this time for mso filters sheet

        ### Create EPG Contracts variables file
        mso_epg_contracts_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="EPG Contracts"
        )
        # add to the dictionary of sheets
        self.dict_of_sheets['mso_epg_contracts_sheet'] = mso_epg_contracts_sheet
        # not going to write a yml file here at this time for mso filters sheet


    def return_dict_of_sheet(self):
        '''
        just returns the dictionary of sheets
        '''
        return self.dict_of_sheets

    def float_to_int(self, sheet):
        '''
        goes through a dictionary and converts floats to ints
        return: sheet - object has changed any floats to ints
        '''
        for key, value in sheet.items():
            if isinstance(value, float):
                sheet[key] = int(value)
        return sheet

    def create_full_list(self, sheet):
        '''
        Reads through the passed sheet object, puts it into a dictionary of lists then returns
        return: full_list - the full dictionary of lists for the data
        '''
        # full_list will hold all the data here we parse out
        full_list = {}
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # we need to put into the dictionary a list depending on the site name
            # if in the dictionary the site name list exists we just append to it
            if data['Site'] in full_list:
                full_list[data['Site']].append(data)
            # if it does NOT exist, we need to create the list and add the data to it
            else:
                full_list[data['Site']] = [data]
            # return the full_list
        return full_list

    def get_apic_ip(self, sheet):
        '''
        simple task, read the APIC tab, add to a variable file called apic_hosts.yml
        '''
        # full_list makes each host an individual item in a dictionary
        # we need to do this to make it iterable later in ansible
        # todo: make this prettier as this full_list part is ugly has to be a better way to do this
        # full list will store the a key called APIC under which each entry will reside with a top key
        # of the controller name
        full_list = {}
        # site_list is just a list of the site names in a file for ansible to use
        site_list = {"SITE_LIST": []}
        full_path = self.ansible_variable_folder + "apic_host_ip_variables.yml"
        site_full_path = self.ansible_variable_folder + "site_list.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # we need to put into the dictionary a list depending on the site name
            # if in the dictionary the site name list exists we just append to it
            if data['Site'] in full_list:
                full_list[data['Site']].append(data)
            # if it does NOT exist, we need to create the list and add the data to it
            else:
                full_list[data['Site']] = [data]
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

        # a secondary item we do is actually right out a yml file that is just the site list to be used later
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # add the entry to the dictionary of lists
            site_list["SITE_LIST"].append(data['Site'])
        # write the info to an ansible variable doc
        with open(site_full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(site_list))

    def interface_policy_groups(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used for IPGs
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        ipg_full_list = {}
        spine_ipg_full_list = {}
        vpc_ipg_full_list = {}
        # write the info to an ansible variable doc
        ipg_full_path = self.ansible_variable_folder + "interface_policy_groups_variables.yml"
        vpc_ipg_full_path = self.ansible_variable_folder + "vpc_interface_policy_groups_variables.yml"
        spine_ipg_full_path = self.ansible_variable_folder + "spine_interface_policy_groups_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # if its a vpc we add to the vpc ipg list
            if data["Type"] == "vpc":
                # now we have to see if the data for the vpc ipg is in the site list yet
                if data['Site'] in vpc_ipg_full_list:
                    vpc_ipg_full_list[data['Site']].append(data)
                # if it does NOT exist, we need to create the list and add the data to it
                else:
                    vpc_ipg_full_list[data['Site']] = [data]
            # if its a normal leaf interface policy group add here
            elif data["Type"] == "leaf":
                # now we have to see if the data for the leaf ipg is in the site list yet
                if data['Site'] in ipg_full_list:
                    ipg_full_list[data['Site']].append(data)
                # if it does NOT exist, we need to create the list and add the data to it
                else:
                    ipg_full_list[data['Site']] = [data]
            # if its a spine interface policy group add here
            elif data["Type"] == "spine":
                # now we have to see if the data for the spine ipg is in the site list yet
                if data['Site'] in spine_ipg_full_list:
                    spine_ipg_full_list[data['Site']].append(data)
                # if it does NOT exist, we need to create the list and add the data to it
                else:
                    spine_ipg_full_list[data['Site']] = [data]
        # after all is said and done, lets add to the files respectively
        with open(ipg_full_path, "w") as file:
            file.write(yaml.dump(ipg_full_list))
        with open(vpc_ipg_full_path, "w") as file:
            file.write(yaml.dump(vpc_ipg_full_list))
        with open(spine_ipg_full_path, "w") as file:
            file.write(yaml.dump(spine_ipg_full_list))

    def aaep_vlan_pool_physical_domain(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "aaep_vlan_pool_physical_domain_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def fabric_nodes(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "fabric_nodes_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def bgp_route_reflectors(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "bgp_route_reflectors_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def leaf_switch_profiles(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "leaf_switch_profiles_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def spine_switch_profiles(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "spine_switch_profiles_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def pod_policy_ntp(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "ntp_pod_policy_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def multisite_apic(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "multisite_apic_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def mso_hosts(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = "provision_mso/mso_hosts_inventory.yml"

        # Nothing fancy here just writing some direct text to a file, lets make our host variables first
        mso_hosts = []
        # loop through hosts in the sheet
        for mso_host in sheet:
            if mso_host["leader or follower"] == "leader":
                mso_hosts.append("[mso_leader]\n{mso_host}\n\n".format(mso_host=mso_host['MSO Server IP']))
        # leader is taken care of now write the followers
        mso_hosts.append("[mso_followers]\n")
        for mso_host in sheet:
            if mso_host["leader or follower"] == "follower":
                mso_hosts.append("{mso_host}\n".format(mso_host=mso_host['MSO Server IP']))
        # now write that to the inventory file
        with open(full_path, "w") as file:
            for line in mso_hosts:
                file.write(line)

    def mso_tenants(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "mso_tenants_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        # we have to format this one a bit differently than most the key needs to be the tenant itself
        # call to the create_full_list function to get the data to write to our file
        full_list = {"Tenants": []}
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # we need to put into the dictionary a list depending on the site name
            # if in the dictionary the site name list exists we just append to it
            if data['Tenant Name'] not in full_list['Tenants']:
                full_list['Tenants'].append(data['Tenant Name'])
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def mso_schemas(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_path = self.ansible_variable_folder + "mso_schemas_variables.yml"
        # call to the create_full_list function to get the data to write to our file
        full_list = self.create_full_list(sheet=sheet)

        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))