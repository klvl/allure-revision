import os
import pathlib
import argparse
import json

from datetime import datetime
from default_config import *


class ArgumentsParser:
    def __init__(self):
        self.args = self.get_args()
        self.spreadsheet_id = self.get_spreadsheet_id()
        self.config = self.get_config()
        self.token = self.get_token()
        self.test_cases_path = self.get_test_cases_dir()
        self.sheet_name = self.get_sheet_name()

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--report', help='path to allure-report. If not specified, the directory where script is '
                                             'running from, will be taken')
        parser.add_argument('--id', help='spreadsheet ID. If not specified, will be taken from config.json. If it is '
                                         'passed as argument and exists in config — the value from argument will be '
                                         'used!')
        parser.add_argument('--token', help='refresh token to use app without Google login. Run app the first time and '
                                            'get refresh_token in the output. Can be passed in config.json')
        parser.add_argument('--sheet', help='specify sheet name. Current date and time is taken if not specified')
        parser.add_argument('--config', help='path to config.json. If not specified, the directory where script is '
                                             'running from, will be taken')
        return parser.parse_args()

    def get_spreadsheet_id(self):
        if self.args.id:  # if --sheet argument was passed
            return self.args.id
        else:
            return False

    def get_config(self):
        # Parse config path
        if self.args.config:  # if --config argument was passed
            path = self.args.config
        else:
            path = 'config.json'

        if os.path.exists(path):  # check if path exists
            path = pathlib.Path(path)
        else:
            path = None

        # Parse config
        if path is not None:
            file = open(path)
            return json.load(file)
        else:
            return DEFAULT_CONFIG

    def get_token(self):
        if self.args.token:
            return self.args.token

        try:
            self.config['token']
        except KeyError:
            return None

        if self.config['token'] != '':
            return self.config['token']
        else:
            print('The "token" value cannot be empty in config.json!')
            exit()

    def get_test_cases_dir(self):
        # If there is no token, then it is initialization run
        if self.token is None:
            return None

        if self.args.report:  # if --report argument was passed
            if self.args.report[len(self.args.report) - 1] == '/':  # Check if last char is '/'
                path = self.args.report + "data/test-cases/"
            else:
                path = self.args.report + "/data/test-cases/"
        else:
            path = 'allure-report/data/test-cases/'

        if os.path.exists(path):  # check if path exists
            return pathlib.Path(path)
        else:
            print('The ' + path + ' path does not exist!')
            exit()

    def get_sheet_name(self):
        if self.args.sheet:  # if --sheet argument was passed
            return self.args.sheet
        else:
            return datetime.now().strftime("%m/%d/%y | %H:%M:%S")

