import os
import pathlib
import argparse
from datetime import datetime


class ArgumentsParser:
    def __init__(self):
        self.args = self.get_args()

        self.spreadsheet_id = self.get_spreadsheet_id()
        self.sheet_name = self.get_sheet_name()
        self.test_cases_path = self.get_test_cases_dir()
        self.config_path = self.get_config_path()

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--sheet', help='specify sheet name. Current date and time is taken if not specified')
        parser.add_argument('--report', help='path to allure-report. If not specified, the directory where script is '
                                             'running from, will be taken')
        parser.add_argument('--config', help='path to config.json. If not specified, the directory where script is '
                                             'running from, will be taken')
        parser.add_argument('--id', help='spreadsheet ID. If not specified, will be taken from config.json. If it is '
                                         'passed as argument and exists in config — the value from argument will be '
                                         'used!')
        return parser.parse_args()

    @staticmethod
    def get_path(path):
        if os.path.exists(path):  # check if path exists
            return pathlib.Path(path)
        else:
            print('The ' + path + ' path does not exist!')
            exit()

    def get_spreadsheet_id(self):
        if self.args.id:  # if --sheet argument was passed
            return self.args.id
        else:
            return False

    def get_sheet_name(self):
        if self.args.sheet:  # if --sheet argument was passed
            return self.args.sheet
        else:
            return datetime.now().strftime("%m/%d/%y | %H:%M:%S")

    def get_test_cases_dir(self):
        if self.args.report:  # if --report argument was passed
            if self.args.report[len(self.args.report) - 1] == '/':  # Check if last char is '/'
                path = self.args.report + "data/test-cases/"
            else:
                path = self.args.report + "/data/test-cases/"
        else:
            path = 'allure-report/data/test-cases/'

        return self.get_path(path)

    def get_config_path(self):
        if self.args.config:  # if --config argument was passed
            path = self.args.config
        else:
            path = 'config.json'

        return self.get_path(path)
