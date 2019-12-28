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

    def read_workbook(self):
        '''
        Read in the ACI workbook and return a dictionary per tab named after the tab
        '''
        # open the aaep_vlan_pool_physical_domain sheet
        aaep_vlan_pool_physical_domain_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="AAEP Domain Pool"
        )
        # we need to pass on the sheet for AAEP/vlan pool/physical domain
        self.aaep_vlan_pool_physical_domain(sheet=aaep_vlan_pool_physical_domain_sheet)

        ### open the interface policy groups sheet
        interface_policy_groups_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Interface Policy Groups"
        )
        # we need to pass the sheet for Interface Policy Groups
        self.interface_policy_groups(sheet=interface_policy_groups_sheet)

        ### open the APIC sheet
        apic_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="APIC"
        )
        # we need to pass the sheet for APIC
        self.get_apic_ip(sheet=apic_sheet)

        ### open the Fabric Switches sheet
        fabric_switches_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Fabric Switches"
        )
        # we need to pass the sheet for Fabric Nodes
        self.fabric_nodes(sheet=fabric_switches_sheet)

        ### open the Pod Policies BGP RR sheet
        bgp_route_reflector_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Pod Policy BGP RR"
        )
        # we need to pass the sheet for the BGP Route Reflectors
        self.bgp_route_reflectors(sheet=bgp_route_reflector_sheet)

        ### open the Leaf Switch Profile Sheet
        switch_profile_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Leaf Switch Profiles"
        )
        # we need to pass the sheet for the Switch Profile
        self.leaf_switch_profiles(sheet=switch_profile_sheet)

        ### open the Pod Policies NTP Sheet
        pod_policy_ntp_sheet = self.xlobject.fetch_data_by_column_by_sheet_name(
            file_path=self.workbook,
            sheet_name="Pod Policies NTP"
        )
        # we need to pass the sheet for the Pod Policies NTP
        self.pod_policy_ntp(sheet=pod_policy_ntp_sheet)

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
        vpc_ipg_full_list = {}
        # write the info to an ansible variable doc
        ipg_full_path = self.ansible_variable_folder + "interface_policy_groups_variables.yml"
        vpc_ipg_full_path = self.ansible_variable_folder + "vpc_interface_policy_groups_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # if its a vpc we add to the vpc ipg list, if its just a leaf policy group add to normal ipg
            if data["Type"] == "vpc":
                # now we have to see if the data for the vpc ipg is in the site list yet
                if data['Site'] in vpc_ipg_full_list:
                    vpc_ipg_full_list[data['Site']].append(data)
                # if it does NOT exist, we need to create the list and add the data to it
                else:
                    vpc_ipg_full_list[data['Site']] = [data]
            elif data["Type"] == "leaf":
                # now we have to see if the data for the leaf ipg is in the site list yet
                if data['Site'] in ipg_full_list:
                    ipg_full_list[data['Site']].append(data)
                # if it does NOT exist, we need to create the list and add the data to it
                else:
                    ipg_full_list[data['Site']] = [data]
        # after all is said and done, lets add to the files respectively
        with open(ipg_full_path, "w") as file:
            file.write(yaml.dump(ipg_full_list))
        with open(vpc_ipg_full_path, "w") as file:
            file.write(yaml.dump(vpc_ipg_full_list))

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
