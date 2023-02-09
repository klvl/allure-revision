import json


class ReportParser:
    def __init__(self, report_path, config):
        self.report_path = report_path
        self.config = config
        self.rows = []
        self.retry_ref = []

    def get_rows(self):
        # Add header row
        header = []
        for column in self.config.columns:
            header.append(column['columnName'])
        self.rows.append(header)

        # Iterate through given path
        for file in self.report_path.iterdir():
            if not file.is_dir():
                # Open file and load json data object
                f = open(file)
                data = json.load(f)

                # Get row
                row = self.get_row(data)

                # Continue loop if row is empty, otherwise, add row, to final list of rows
                if not row:
                    continue
                else:
                    self.rows.append(row)

        # Validate failed tests found
        found_tests_amount = len(self.rows) - 1  # All rows without header line
        if not found_tests_amount:
            print('No tests with ' + str(self.config.statuses) + ' status(-es) found!')
            exit()
        print('There were ' + str(found_tests_amount) + ' tests with ' + str(self.config.statuses) +
              ' status(-es) found!')

        return self.rows

    def get_row(self, data):
        row = []
        # Get STATUS and TEST name
        status = self.get_status(data)
        test_name = self.get_test_name(data)

        # Remove test from final rows, if a current test is newer(was retried in test run)
        if self.is_test_already_present(test_name):
            if self.is_existing_test_is_older(test_name, data):
                self.remove_existing(test_name)
            else:
                return row

        # If status is passed return empty row
        if status in self.config.statuses:
            for column in self.config.columns:
                # Add empty row
                if not column['reportValue']:
                    row.append('')

                # Add TEST name to row array
                if column['reportValue'] == 'fullName':
                    row.append(test_name)

                # Get MESSAGE and add to row array
                if column['reportValue'] == 'message':
                    message = self.get_message(data)
                    row.append(message)

                # Get CATEGORY and add to row array
                if column['reportValue'] == 'category':
                    category = self.get_category(data)
                    row.append(category)

                # Add STATUS to row array
                if column['reportValue'] == 'status':
                    row.append(status)

        # Collect test name and stop time
        self.collect_retry_ref(data)
        return row

    def collect_retry_ref(self, data):
        name = self.get_test_name(data)
        stop = self.get_stop_time(data)
        self.retry_ref.append({'name': name, 'stop_time': stop})

    def get_ref_stop_time(self, test_name):
        for ref in self.retry_ref:
            if ref['name'] == test_name:
                return ref['stop_time']

    def is_test_already_present(self, test_name):
        for row in self.retry_ref:
            if row['name'] == test_name:
                return True
        return False

    def is_existing_test_is_older(self, test_name, data):
        ref_stop = self.get_ref_stop_time(test_name)
        actual_stop = self.get_stop_time(data)
        return ref_stop < actual_stop

    def remove_existing(self, test_name):
        for row in self.rows:
            if row[0] == test_name:
                self.rows.remove(row)

    @staticmethod
    def get_test_name(data):
        return data['fullName']

    @staticmethod
    def get_message(data):
        return data['statusMessage'].partition('\n')[0]

    @staticmethod
    def get_category(data):
        result = "Unknown"
        for category in data['extra']['categories']:
            if 'messageRegex' in category:
                result = category['name']
        return result

    @staticmethod
    def get_status(data):
        return data['status']

    @staticmethod
    def get_stop_time(data):
        return data['time']['stop']
