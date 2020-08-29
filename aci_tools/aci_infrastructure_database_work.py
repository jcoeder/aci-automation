import sqlite3
import aci_tools
import sys


class ACI_Infrastructure_Database():

    def __init__(self):
        self.aci_database = "aci_database.db"

    def output_dict(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect_to_database(self):
        '''
        This will connect to a database and return the connection object
        '''
        # connect to database and get cursor
        db_connection = sqlite3.connect(self.aci_database)
        db_connection.row_factory = self.output_dict
        return db_connection


    def create_and_initialize_database(self):
        '''
        if the SQL database doesn't exist, lets build it and set up our tables
        '''
        # pre-build out our table statements
        table_list = {}
        table_list['create_sites_table'] = "CREATE TABLE IF NOT EXISTS sites (site text PRIMARY KEY, site_id text);"
        table_list['create_schemas_table'] = '''CREATE TABLE IF NOT EXISTS schemas (
                                                                    site text NOT NULL,
                                                                    schema text PRIMARY KEY,
                                                                    schema_id text,
                                                                    FOREIGN KEY (site) REFERENCES sites (site)
                                                                    );'''
        table_list['create_tenants_table'] = '''CREATE TABLE IF NOT EXISTS tenants (
                                                                    site text NOT NULL,
                                                                    tenant text PRIMARY KEY,
                                                                    tenant_id text,
                                                                    FOREIGN KEY (site) REFERENCES sites (site)
                                                                    );'''
        table_list['create_vrfs_table'] = '''CREATE TABLE IF NOT EXISTS vrfs (
                                                                tenant text NOT NULL,
                                                                vrf_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                vrf text NOT NULL,
                                                                FOREIGN KEY (tenant) REFERENCES tenants (tenant)
                                                                );'''
        table_list['create_bridge_domains_table'] = '''CREATE TABLE IF NOT EXISTS bridge_domains(
                                                                tenant text NOT NULL,
                                                                bridge_domain_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                bridge_domain text NOT NULL,
                                                                subnet text,
                                                                vrf text,
                                                                FOREIGN KEY (tenant) REFERENCES tenants (tenant)
                                                                );'''
        table_list['create_filters_table'] = '''CREATE TABLE IF NOT EXISTS filters(
                                                                tenant text NOT NULL,
                                                                filter text NOT NULL,
                                                                filter_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                filter_entry_name text,
                                                                ethertype text,
                                                                dest_port_begin text,
                                                                dest_port_end text,
                                                                ip_protocol text,
                                                                FOREIGN KEY (tenant) REFERENCES tenants (tenant)
                                                                );'''
        table_list['create_contracts_table'] = '''CREATE TABLE IF NOT EXISTS contracts(
                                                                tenant text NOT NULL,
                                                                contract text NOT NULL,
                                                                contract_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                contract_scope text NOT NULL,
                                                                FILTER text,
                                                                FOREIGN KEY (tenant) REFERENCES tenants (tenant)
                                                                );'''
        table_list['create_application_profiles_table'] = '''CREATE TABLE IF NOT EXISTS application_profiles(
                                                                tenant text NOT NULL,
                                                                application_profile_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                application_profile text NOT NULL,
                                                                FOREIGN KEY (tenant) REFERENCES tenants (tenant)
                                                                );'''
        table_list['create_epgs_table'] = '''CREATE TABLE IF NOT EXISTS epgs(
                                                             epg_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             application_profile text NOT NULL,
                                                             epg text NOT NULL,
                                                             FOREIGN KEY (application_profile) REFERENCES application_profiles (application_profile)
                                                             );'''
        table_list['create_epg_contracts_table'] = '''CREATE TABLE IF NOT EXISTS epg_contracts(
                                                             epg_contract_map_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             epg text NOT NULL,
                                                             contract text NOT NULL,
                                                             provider_or_consumer text NOT NULL,
                                                             FOREIGN KEY (epg) REFERENCES epgs (epg)
                                                             );'''

        # connection object and cursor object
        db_connection = self.connect_to_database()
        db_cursor = db_connection.cursor()
        # create all the tables
        for key, value in table_list.items():
            db_cursor.execute(value)
            # commit the changes
            db_connection.commit()

        # close the connection
        db_cursor.close()

    def strip_characters(self, char_list=[",\)\("], input_item=None):
        '''
        pass me an item, i'll go through and remove a characters given and return it
        '''
        if type(input_item) == "list":
            sanitized_item = [i.replace(char_list, "") for i in input_item]
        elif type(input_item) == "str":
            sanitized_item = input_item.replace(char_list, "")
        return sanitized_item

    def read_database(self):
        '''
        Just read and print the database for debugging purposes
        '''
        # connect to database and get cursor
        db_connection = self.connect_to_database()
        db_cursor = db_connection.cursor()
        # execute the cursor object
        db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # fetch all the output and print it
        for table in db_cursor.fetchall():
            db_cursor.execute("select * from {table};".format(table=table['name']))
            print(db_cursor.fetchall())

        # close the connection
        db_connection.close()

    def check_for_existence(self, db_cursor, query):
        '''
        pass me a query and i'll do a fetchone() to see if the item exists
        '''
        # run the query and check if we got anything
        db_cursor.execute(query)
        if not db_cursor.fetchone():
            return True

    def write_from_excel_to_database(self, dict_of_sheets):
        '''
        read the excel sheet and write to the database
        '''
        # Get our connection object and cursor
        # Outer try
        try:
            db_connection = self.connect_to_database()
            db_cursor = db_connection.cursor()
            try:
                # this opens up the dictionary of lists passed with the key named apic_sheet which holds
                # individual entries of dictionaries inside.  So outer dict, then list that then holds dict per site
                for i in dict_of_sheets['apic_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM sites WHERE site='{site_name}'".format(site_name=i['Site'])
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = "INSERT INTO sites ('site') VALUES ('{site_name}');".format(site_name=i['Site'])
                        # write and commit changes to the database
                        db_cursor.execute(insert)
                        db_connection.commit()

                # schemas table now
                for i in dict_of_sheets['mso_schemas_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM schemas WHERE schema='{schema_name}';".format(
                        schema_name=i['Schema Name']
                    )
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO schemas ('site', 'schema') VALUES ('{site_name}','{schema}');'''.format(
                            site_name=i['Site'], schema=i['Schema Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # tenants table now
                for i in dict_of_sheets['mso_tenants_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM tenants WHERE tenant='{tenant_name}';".format(
                        tenant_name=i['Tenant Name']
                    )
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO tenants ('site', 'tenant') VALUES ('{site_name}','{tenant}');'''.format(
                            site_name=i['Site'], tenant=i['Tenant Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # vrfs table now
                for i in dict_of_sheets['mso_schemas_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM vrfs WHERE vrf='{vrf_name}';".format(
                        vrf_name=i['VRF']
                    )
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO vrfs ('vrf', 'tenant') VALUES ('{vrf_name}', '{tenant}');'''.format(
                            vrf_name=i['VRF'], tenant=i['Tenant Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # bridge_domains table now
                for i in dict_of_sheets['mso_schemas_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM bridge_domains WHERE bridge_domain='{bridge_domain}';".format(
                        bridge_domain=i['Bridge Domain']
                    )
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO bridge_domains ('bridge_domain', 'tenant', 'subnet', 'vrf') 
                                    VALUES ('{bridge_domain}', '{tenant}', '{subnet}', '{vrf_name}');'''.format(
                                    vrf_name=i['VRF'], tenant=i['Tenant Name'],
                                    bridge_domain=i['Bridge Domain'], subnet=i['Subnet IP and CIDR']
                        )
                        db_cursor.execute(insert)
                        db_connection.commit()

                # filters table now
                for i in dict_of_sheets['mso_filters_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = "SELECT * FROM filters WHERE filter_entry_name='{filter_entry_name}';".format(
                        filter_entry_name=i['Filter Entry Name']
                    )
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO filters ('filter', 'tenant', 'ethertype', 'dest_port_begin',
                        'dest_port_end', 'ip_protocol', 'filter_entry_name') VALUES ('{filter}', '{tenant}',
                        '{ethertype}', '{dest_port_begin}', '{dest_port_end}', '{ip_protocol}',
                        '{filter_entry_name}');'''.format(filter=i['Filter'], tenant=i['Tenant Name'],
                         ethertype=i['Ethertype'], dest_port_begin=i['Destination Port Begin'],
                         dest_port_end=i['Destination Port End'], ip_protocol=i['IP Protocol'],
                         filter_entry_name=i['Filter Entry Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # contract table now
                for i in dict_of_sheets['mso_contracts_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = '''SELECT * FROM contracts WHERE contract = '{contract}' AND tenant = '{tenant}'
                    AND contract_scope = '{contract_scope}' AND filter = '{filter}';'''.format(filter=i['Filter'],
                            contract=i['Contract'], contract_scope=i['Contract Scope'], tenant=i['Tenant Name'])
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO contracts ('contract', 'tenant', 'contract_scope', 'filter') VALUES
                        ('{contract}', '{tenant}', '{contract_scope}', '{filter}');'''.format(
                            filter=i['Filter'], contract=i['Contract'], contract_scope=i['Contract Scope'],
                            tenant=i['Tenant Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # application profiles now
                for i in dict_of_sheets['mso_schemas_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = '''SELECT * FROM application_profiles WHERE tenant = '{tenant}' AND 
                    application_profile = '{application_profile}';'''.format(tenant=i['Tenant Name'],
                    application_profile=i['ANP Name'])
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO application_profiles ('application_profile', 'tenant') VALUES
                        ('{application_profile}', '{tenant}');'''.format(application_profile=i['ANP Name'],
                            tenant=i['Tenant Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # epgs now
                for i in dict_of_sheets['mso_schemas_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = '''SELECT * FROM epgs WHERE epg = '{epg}' AND 
                    application_profile = '{application_profile}';'''.format(application_profile=i['ANP Name'],
                    epg=i['EPG Name'])
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO epgs ('application_profile', 'epg') VALUES
                        ('{application_profile}', '{epg}');'''.format(application_profile=i['ANP Name'],
                            epg=i['EPG Name'])
                        db_cursor.execute(insert)
                        db_connection.commit()

                # epgs contracts now
                for i in dict_of_sheets['mso_epg_contracts_sheet']:
                    # Make sure that an entry doesn't exist before we try to insert
                    exist_check = '''SELECT * FROM epg_contracts WHERE epg = '{epg}' AND contract = '{contract}' AND
                     provider_or_consumer = '{provider_or_consumer}';'''.format(epg=i['EPG Name'],
                    contract=i['Contract'], provider_or_consumer=i['Provider or Consumer'])
                    # if we got a True back then it doesn't exist
                    if self.check_for_existence(query=exist_check, db_cursor=db_cursor):
                        insert = '''INSERT INTO epg_contracts ('epg', 'contract', 'provider_or_consumer') VALUES
                        ('{epg}', '{contract}', '{provider_or_consumer}');'''.format(epg=i['EPG Name'],
                            contract=i['Contract'], provider_or_consumer=i['Provider or Consumer'])
                        db_cursor.execute(insert)
                        db_connection.commit()



            except Exception as e:
                # catch sql insert related exceptions
                print(e)

            finally:
                db_connection.close()

        # Outer Exception for outer try
        except Exception as e:
            # catch connecting to sql database exceptions here
            print(e)
            # no need to continue if the database connection failed
            sys.exit()

        # write first to the site database








# if we were called direct
if __name__ == "__main__":
    aci_db = ACI_Infrastructure_Database()
    # make that database
    aci_db.create_and_initialize_database()
    aci_db.read_database()
