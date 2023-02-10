import json

from vars import *


class ConfigParser:
    def __init__(self, config_path, spreadsheet_id_from_args, token_from_args):
        self.config = self.init_config(config_path)
        self.spreadsheet_id = self.init_spreadsheet_id(spreadsheet_id_from_args)
        self.statuses = self.init_statuses()
        self.colors = COLORS
        self.column_names = COLUMN_NAMES
        self.columns = self.init_columns()
        self.creds = CREDS
        self.token = self.init_token(token_from_args)

    @staticmethod
    def init_config(config_path):
        if config_path is not None:
            file = open(config_path)
            return json.load(file)
        else:
            return DEFAULT_CONFIG

    def init_spreadsheet(self):
        try:
            return self.config['spreadsheet']
        except KeyError:
            print('There is no "spreadsheet" parameter in config.json!')
            exit()

    def init_spreadsheet_id(self, spreadsheet_id_from_args):
        if spreadsheet_id_from_args:
            return spreadsheet_id_from_args

        try:
            return self.config['spreadsheet']['id']
        except KeyError:
            print('The "spreadsheet.id" should be passed as --id argument or be specified in config.json!')
            exit()

    def init_statuses(self):
        statuses = None
        try:
            statuses = self.config['statuses']
        except KeyError:
            print('There is no "statuses" parameter in config.json!')
            exit()

        # Validate all statuses are expected
        for status in statuses:
            if status != 'failed' and status != 'passed' and status != 'skipped' and status != 'broken' and \
                    status != 'unknown':
                print('The status "' + status + '" is not expected! '
                                                'Should be one of the following: failed, passed, skipped, broken')
                exit()

        # Validate statuses are unique
        for status in statuses:
            status_duplication = 0
            for s in statuses:
                if s == status:
                    status_duplication += 1
            if status_duplication > 1:
                print('The status "' + status + '" is duplicated!')
                exit()

        return statuses

    def init_columns(self):
        columns = None

        # Validate 'column' exist
        try:
            columns = self.config['columns']
        except KeyError:
            print('There is no "columns" parameter in config.json!')
            exit()

        # Validate columns are not empty
        if not columns:
            print('The "columns" array cannot be empty!')
            exit()

        # Validate columns do not exceed maximum allowed amount
        if len(columns) > len(self.column_names):
            print('The maximum supported columns amount is 15! '
                  'Try less amount of columns or wait for the next release!')
            exit()

        # Validate all columns have 'name' param
        for column in columns:
            try:
                column['name']
            except KeyError:
                print('The "column.name" param is set not for all columns in config.json!')
                exit()

        # Validate all columns have 'index' param
        for column in columns:
            try:
                column['index']
            except KeyError:
                print('The "index" param is set not for all columns in config.json!')
                exit()

        # Validate indexes are unique
        for column in columns:
            index_duplication = 0
            for c in columns:
                if c['index'] == column['index']:
                    index_duplication += 1

            if index_duplication > 1:
                print('The index ' + str(column['index']) + ' is duplicated!')
                exit()

        # Check if reportValue is valid in all columns
        for column in columns:
            try:
                if column['reportValue'] not in AVAILABLE_REPORT_VALUES:
                    print('The reportValue "' + column['reportValue'] + '" is not valid in config.json!\n' +
                          'Permitted values: ' + str(AVAILABLE_REPORT_VALUES))
                    exit()
            except KeyError:
                continue

        # Set empty reportValues
        for column in columns:
            try:
                column['reportValue']
            except KeyError:
                column['reportValue'] = False
                
        # Set empty sizes
        for column in columns:
            try:
                column['size']
            except KeyError:
                column['size'] = False

        # Validate conditional formatting
        for column in columns:
            try:
                rules = column['conditionalFormatting']
                for rule in rules:
                    try:
                        if rule['color'] not in self.colors.keys():
                            print('The color "' + rule['color'] + '" is not available yet! ' +
                                  'Try one of the following:\n' + str(self.colors.keys()))
                    except KeyError:
                        print('There is no color attribute in config.json! Affected column:\n' + column)
                        exit()
                    try:
                        rule['ifValue']
                    except KeyError:
                        print('The ifValue parameter should be present in conditionalFormatting in config.json!')
            except KeyError:
                column['conditionalFormatting'] = False  # Set empty conditional formatting

        # Sort columns by index
        final_columns = []
        for i in range(len(columns)):
            for column in columns:
                if column['index'] == i:
                    final_columns.append(column)

        return final_columns

    def init_token(self, token_from_args):
        if token_from_args is not None:
            TOKEN['refresh_token'] = token_from_args
            return TOKEN
        else:
            try:
                TOKEN['refresh_token'] = self.config['spreadsheet']['refresh_token']
                return TOKEN
            except KeyError:
                return None

