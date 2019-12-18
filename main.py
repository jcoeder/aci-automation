# Main class

import aci_tools
import argparse

class Main():

    def __init__(self):
        # base folder to store variables in after generated to be used by ansible
        self.ansible_variables_folder = "ansible playbooks/ansible variables/"
        # lets see why we"re being called
        parser = argparse.ArgumentParser()
        # store_true lets the argument default to False unless passed then it becomes True
        parser.add_argument("--aci_excel_sheet", type=str,
                            help="the spreadsheet to read info from for the aci build out")
        self.args = parser.parse_args()

    def do_work(self):
        # start the switching of options we could do
        if self.args.aci_excel_sheet:
            # create object of
            workbook = aci_tools.excel_workbook_read.ACI_Workbook_Read(
                workbook=self.args.aci_excel_sheet,
                ansible_variable_folder=self.ansible_variables_folder
            )
            # read the workbook
            workbook.read_workbook()


if __name__ == "__main__":
    main = Main()
    main.do_work()