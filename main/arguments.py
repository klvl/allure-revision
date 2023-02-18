import argparse


class ArgumentsParser:
    def __init__(self):
        self.args = self.get_args()
        self.spreadsheet_id = self.get_spreadsheet_id()
        self.config_path = self.get_config_path()
        self.token = self.get_token()
        self.report_path = self.get_allure_report_path()
        self.sheet_name = self.get_sheet_name()
        self.sheet_index = self.get_sheet_index()

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--report_path', help='path to allure-report. If not specified, the directory ' +
                                                  'where script is running from, will be taken.')
        parser.add_argument('--id', help='spreadsheet ID. If not specified, will be taken from config.json. If it is '
                                         'passed as argument and exists in config — the value from argument will be '
                                         'used.')
        parser.add_argument('--token', help='refresh token to use app without Google login. Run app the first time and '
                                            'get refresh_token in the output. Can be passed in config.json.')
        parser.add_argument('--sheet_name', help='specify sheet name. Current date and time is taken if not specified.')
        parser.add_argument('--sheet_index', help='specify where index of new sheet among other sheets in a ' +
                                                  'spreadsheet. The sheet index will be 0 if not specified.')
        parser.add_argument('--config_path', help='path to config.json. If not specified, the directory where script ' +
                                                  'is running from, will be taken.')
        return parser.parse_args()

    def get_spreadsheet_id(self):
        if self.args.id:
            return self.args.id
        else:
            return False

    def get_config_path(self):
        if self.args.config_path:
            return self.args.config_path
        else:
            return False

    def get_token(self):
        if self.args.token:
            return self.args.token
        else:
            return False

    def get_sheet_name(self):
        if self.args.sheet_name:
            return self.args.sheet_name
        else:
            return False

    def get_sheet_index(self):
        if self.args.sheet_index:
            return self.args.sheet_index
        else:
            return False

    def get_allure_report_path(self):
        if self.args.report_path:
            return self.args.report_path
        else:
            return False

