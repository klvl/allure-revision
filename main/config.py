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
            formatting = self.config['headerFormatting']
        except KeyError:
            return False

        # Validate background color
        try:
            if formatting['backgroundColor'] not in COLORS.keys():
                print('The color "' + formatting['backgroundColor'] + '" is not available yet! ' +
                      'Try one of the following:\n' + str(COLORS.keys()))
                exit()
        except KeyError:
            print('The backgroundColor is not present in headerFormatting!')
            exit()

        # Validate foreground color
        try:
            if formatting['foregroundColor'] not in COLORS.keys():
                print('The color "' + formatting['backgroundColor'] + '" is not available yet! ' +
                      'Try one of the following:\n' + str(COLORS.keys()))
                exit()
        except KeyError:
            print('The foregroundColor is not present in headerFormatting!')
            exit()

        # Validate font size
        try:
            formatting['fontSize']
        except KeyError:
            print('The fontSize is not present in headerFormatting!')
            exit()

        return formatting

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

        # Validate conditional formatting
        for column in columns:
            try:
                rules = column['conditionalFormatting']
                for rule in rules:
                    try:
                        if rule['color'] not in COLORS.keys():
                            print('The color "' + rule['color'] + '" is not available yet! ' +
                                  'Try one of the following:\n' + str(COLORS.keys()))
                    except KeyError:
                        print('There is no color attribute in config.json! Affected column:\n' + column)
                        exit()
                    try:
                        rule['ifValue']
                    except KeyError:
                        print('The ifValue parameter should be present in conditionalFormatting in config.json!')
            except KeyError:
                column['conditionalFormatting'] = False  # Set empty conditional formatting

        # Validate indexes sequence
        actual_indexes = [column['index'] for column in columns]
        actual_indexes.sort()
        expected_indexes = [index for index in range(len(columns))]
        if actual_indexes != expected_indexes:
            print('Invalid columns indexes sequence!\n\n' +
                  'Actual sequence: ' + str(actual_indexes) + '\n' +
                  'Expected sequence: ' + str(expected_indexes))
            exit()

        # Sort columns by index
        final_columns = []
        for i in range(len(columns)):
            for column in columns:
                if column['index'] == i:
                    final_columns.append(column)

        return final_columns

