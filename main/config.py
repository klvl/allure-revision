import json

from sys import exit
from vars import AVAILABLE_REPORT_STATUSES, AVAILABLE_REPORT_VALUES, AVAILABLE_HORIZONTAL_ALIGNMENTS, COLUMN_NAMES, \
    COLORS


class ConfigParser:
    def __init__(self, config):
        self.config = config
        self.spreadsheet_id = self.get_spreadsheet_id()
        self.token = self.get_token()

    def get_spreadsheet_id(self):
        try:
            return self.config['id']
        except KeyError:
            return False

    def get_token(self):
        token = False
        try:
            if self.config['token']:
                token = self.config['token']
        except KeyError:
            pass

        if token == '':
            print('The "token" value cannot be empty in config.json!')
            exit()
        else:
            return token

    def get_header_formatting(self):
        try:
            return self.get_formatting('headerFormatting', self.config['headerFormatting'])
        except KeyError:
            return False

    def get_new_sheet_index(self):
        try:
            return self.config['newSheetIndex']
        except KeyError:
            return None

    def get_statuses(self):
        statuses = None

        # Validate 'statuses' param exists
        try:
            statuses = self.config['statuses']
        except KeyError:
            print('There is no "statuses" parameter in config.json!')
            exit()

        # Validate 'statuses' are not empty
        if not statuses:
            print('The "statuses" array cannot be empty in config.json!')
            exit()

        # Validate all statuses are expected
        for status in statuses:
            if status not in AVAILABLE_REPORT_STATUSES:
                print('The status "' + status + '" is not expected! ' +
                      'Should be one of the following: ' + str(AVAILABLE_REPORT_STATUSES))
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

    def get_columns(self):
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
        if len(columns) > len(COLUMN_NAMES):
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

        # Check that columns does not contain reportValue and dropdown params together
        for column in columns:
            try:
                if column['reportValue'] is not None and column['dropdown'] is not None:
                    print('It is not allowed to use "reportValue" and "dropdown" parameters together in config.json!')
                    exit()
            except KeyError:
                pass

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

        # Validate horizontal alignments
        for column in columns:
            try:
                if column['horizontalAlignment'] not in AVAILABLE_HORIZONTAL_ALIGNMENTS:
                    print('Invalid "' + column['horizontalAlignment'] + '" + horizontalAlignment value!\n' +
                          'Available values: ' + str(AVAILABLE_HORIZONTAL_ALIGNMENTS))
                    exit()
            except KeyError:
                column['horizontalAlignment'] = False

        # Validate dropdown
        for column in columns:
            try:
                final_dropdown = []
                for item in column['dropdown']:
                    final_dropdown.append({'userEnteredValue': item})
                column['dropdown'] = final_dropdown
            except KeyError:
                column['dropdown'] = False

        # Validate formatting
        for column in columns:
            try:
                if column['formatting']:
                    column['formatting'] = self.get_formatting(column['name'] + '.formatting', column['formatting'])
            except KeyError:
                column['formatting'] = False

        # Validate conditional formatting
        for column in columns:
            try:
                for rule in column['conditionalFormatting']:

                    # Validate color
                    try:
                        self.validate_color('conditionalFormatting.color', rule['color'])
                    except KeyError:
                        print('There is no color attribute in config.json! Affected column:\n' + column)
                        exit()

                    # Validate ifValue
                    try:
                        rule['ifValue']
                    except KeyError:
                        print('The ifValue parameter should be present in conditionalFormatting in config.json!')

            except KeyError:
                column['conditionalFormatting'] = False  # Set empty conditional formatting

        # Set final conditional formatting
        for column in columns:
            try:
                if column['conditionalFormatting']:
                    for rule in column['conditionalFormatting']:
                        if isinstance(rule['color'], dict):
                            rule['color'] = self.set_spreadsheet_color(rule['color'])
                        else:
                            rule['color'] = COLORS[rule['color']]
            except KeyError:
                pass

        return columns

    @staticmethod
    def validate_color(param_name, param_value):
        try:
            if param_value in COLORS:
                return True
        except TypeError:
            pass

        try:
            red = param_value['red']
            green = param_value['green']
            blue = param_value['blue']

            if red > 255:
                print('The "' + param_name + '" contains "red" parameter with value "' + red + '" > 255!\n' +
                      'The custom colors are specified in RGB format!')
                exit()

            if green > 255:
                print('The "' + param_name + '" contains "green" parameter with value "' + green + '" > 255!\n' +
                      'The custom colors are specified in rgb format!')
                exit()

            if blue > 255:
                print('The "' + param_name + '" contains "blue" parameter with value "' + blue + '" > 255!\n' +
                      'The custom colors are specified in rgb format!')
                exit()

        except KeyError:
            print('The "' + param_name + '" parameter should contain one of a pre-defined colors: "' +
                  str(COLORS) + '"!\nAlternatively, you can specify custom color — jon object with "red", ' +
                  '"green" and "blue" parameters!')
            exit()

    def get_formatting(self, path, formatting):
        final_formatting = formatting

        # Validate background color
        try:
            self.validate_color(path + '.backgroundColor', final_formatting['backgroundColor'])
        except KeyError:
            pass

        # Set final background color
        try:
            if isinstance(final_formatting['backgroundColor'], dict):
                final_formatting['backgroundColor'] = self.set_spreadsheet_color(final_formatting['backgroundColor'])
            else:
                final_formatting['backgroundColor'] = COLORS[final_formatting['backgroundColor']]
        except KeyError:
            pass

        # Validate horizontal alignment
        try:
            if final_formatting['horizontalAlignment'] not in AVAILABLE_HORIZONTAL_ALIGNMENTS:
                print('The "' + path + '.horizontalAlignment" value is invalid in config.json!\n' +
                      'Should be one of the following: ' + str(AVAILABLE_HORIZONTAL_ALIGNMENTS) + ' !')
                exit()
        except KeyError:
            pass

        # Validate if textFormat is present
        try:
            final_formatting['textFormat']
        except KeyError:
            return final_formatting

        # Validate foreground color
        try:
            self.validate_color(path + '.textFormat.foregroundColor', final_formatting['textFormat']['foregroundColor'])
        except KeyError:
            pass

        # Set final foreground color
        try:
            if isinstance(final_formatting['textFormat']['foregroundColor'], dict):
                final_formatting['textFormat']['foregroundColor'] = \
                    self.set_spreadsheet_color(final_formatting['textFormat']['foregroundColor'])
            else:
                final_formatting['textFormat']['foregroundColor'] = \
                    COLORS[final_formatting['textFormat']['foregroundColor']]
        except KeyError:
            pass

        # Validate font size
        try:
            if final_formatting['textFormat']['fontSize'] <= 0:
                print('The "' + path + '.headerFormatting.textFormat.fontSize" value should be more then 0!')
                exit()
            elif final_formatting['textFormat']['fontSize'] > 400:
                print('The "' + path + '.headerFormatting.textFormat.fontSize" value should be less then 400!')
        except KeyError:
            pass

        # Validate bold
        try:
            if final_formatting['textFormat']['bold']:
                final_formatting['textFormat']['bold'] = json.dumps(True)
        except KeyError:
            pass
        return final_formatting

    @staticmethod
    def set_spreadsheet_color(colors):
        return {'red': colors['red'] / 255, 'green': colors['green'] / 255, 'blue': colors['blue'] / 255}




