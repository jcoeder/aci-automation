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

    def float_to_int(self, sheet):
        '''
        goes through a dictionary and converts floats to ints
        return: sheet - object has changed any floats to ints
        '''
        for key, value in sheet.items():
            if isinstance(value, float):
                sheet[key] = int(value)
        return sheet

    def get_apic_ip(self, sheet):
        '''
        simple task, read the APIC tab, add to a variable file called apic_hosts.yml
        '''
        # full_list makes each host an individual item in a dictionary
        # we need to do this to make it iterable later in ansible
        # todo: make this prettier as this full_list part is ugly has to be a better way to do this
        # full list will store the a key called APIC under which each entry will reside with a top key
        # of the controller name
        full_list = {"APIC": []}
        full_path = self.ansible_variable_folder + "apic_host_ip_variables.yml"
        with open(full_path, "w") as file:
            for data in sheet:
                # clean the input
                data = self.float_to_int(data)
                # add the entry to the dictionary of lists
                full_list["APIC"].append(data)
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def aaep_vlan_pool_physical_domain(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_list = {"APIC": []}
        full_path = self.ansible_variable_folder + "aaep_vlan_pool_physical_domain_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # add the entry to the dictionary of lists
            full_list["APIC"].append(data)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))

    def interface_policy_groups(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used for IPGs
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        ipg_full_list = {"APIC": []}
        vpc_ipg_full_list = {"APIC": []}
        # write the info to an ansible variable doc
        ipg_full_path = self.ansible_variable_folder + "interface_policy_groups_variables.yml"
        vpc_ipg_full_path = self.ansible_variable_folder + "vpc_interface_policy_groups_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # if its a vpc we add to the vpc ipg list, if its just a leaf policy group add to normal ipg
            if data["Type"] == "vpc":
                vpc_ipg_full_list["APIC"].append(data)
            elif data["Type"] == "leaf":
                ipg_full_list["APIC"].append(data)
        # after all is said and done, lets add to the files respectively
        with open(ipg_full_path, "w") as file:
            file.write(yaml.dump(ipg_full_list))
        with open(vpc_ipg_full_path, "w") as file:
            file.write(yaml.dump(vpc_ipg_full_list))

    def fabric_nodes(self, sheet):
        '''
        Uses the xlsx file to build out the variables and generate a YAML file to be used
        This is used for AAEP, VLAN Pools, and Physical Domains
        '''
        # full_list lets us put together a dictionary of lists to pass to ansible
        full_list = {"APIC": []}
        full_path = self.ansible_variable_folder + "fabric_nodes_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # add the entry to the dictionary of lists
            full_list["APIC"].append(data)
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
        full_list = {"APIC": []}
        full_path = self.ansible_variable_folder + "bgp_route_reflectors_variables.yml"
        for data in sheet:
            # clean the input
            data = self.float_to_int(data)
            # add the entry to the dictionary of lists
            full_list["APIC"].append(data)
        # write the info to an ansible variable doc
        with open(full_path, "w") as file:
            # convert to yaml before writing to sheet
            file.write(yaml.dump(full_list))
