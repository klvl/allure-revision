import os
import json
import pathlib

from arguments import ArgumentsParser
from config import ConfigParser
from default_config import DEFAULT_CONFIG
from vars import TOKEN
from datetime import datetime
from sys import exit


class DataProvider:
    def __init__(self):
        self.args_parser = ArgumentsParser()
        self.config = self.get_config()
        self.config_parser = ConfigParser(self.config)

        self.token = self.get_token()

        if self.token is not None:
            self.spreadsheet_id = self.get_spreadsheet_id()
            self.test_cases_path = self.get_test_cases_path()
            self.sheet_name = self.get_sheet_name()
            self.header_formatting = self.config_parser.get_header_formatting()
            self.new_sheet_index = self.get_new_sheet_index()
            self.statuses = self.config_parser.get_statuses()
            self.columns = self.config_parser.get_columns()
        else:
            self.spreadsheet_id = None
            self.test_cases_path = None
            self.sheet_name = None
            self.header_formatting = None
            self.new_sheet_index = None
            self.statuses = None
            self.columns = None

    def get_config(self):
        if self.args_parser.config_path:
            path = self.args_parser.config_path
        else:
            path = 'config.json'

        if os.path.exists(path):
            path = pathlib.Path(path)
        else:
            path = None

        # Parse config
        if path is not None:
            file = open(path)
            return json.load(file)
        else:
            return DEFAULT_CONFIG

    def get_spreadsheet_id(self):
        if self.args_parser.spreadsheet_id:
            return self.args_parser.spreadsheet_id
        elif self.config_parser.spreadsheet_id:
            return self.config_parser.spreadsheet_id
        else:
            print('The "id" (spreadsheet ID) should be passed as --id argument or be specified in config.json!')
            exit()

    def get_token(self):
        token = None
        if self.args_parser.token:
            token = self.args_parser.token
        elif self.config_parser.token:
            token = self.config_parser.token

        if token is not None:
            TOKEN['refresh_token'] = token
            token = TOKEN

        return token

    def get_test_cases_path(self):
        if self.args_parser.report_path:
            if self.args_parser.report_path[len(self.args_parser.report_path) - 1] == '/':
                path = self.args_parser.report_path + "data/test-cases/"
            else:
                path = self.args_parser.report_path + "/data/test-cases/"
        else:
            path = 'allure-report/data/test-cases/'

        if os.path.exists(path):
            return pathlib.Path(path)
        else:
            print('The ' + path + ' path does not exist! Specify path to allure-report folder by --report CLI option ' +
                  'or put the allure-report folder in current working directory!')
            exit()

    def get_sheet_name(self):
        if self.args_parser.sheet_name:
            return self.args_parser.sheet_name
        else:
            return datetime.now().strftime("%m/%d/%y | %H:%M:%S")

    def get_new_sheet_index(self):
        if self.args_parser.sheet_index:
            return self.args_parser.sheet_index
        else:
            return self.config_parser.get_new_sheet_index()

