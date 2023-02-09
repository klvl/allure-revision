import json


class ConfigParser:
    def __init__(self, config_path):
        self.config = self.init_config(config_path)
        self.spreadsheet_id = self.init_spreadsheet_id()

    @staticmethod
    def init_config(config_path):
        file = open(config_path)
        return json.load(file)

    def init_spreadsheet_id(self):
        try:
            return self.config['spreadsheetId']
        except KeyError:
            print('There is no "spreadsheetId" parameter in config.json!')
            exit()

