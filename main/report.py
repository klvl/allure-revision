import json

from sys import exit


class ReportParser:
    def __init__(self, test_cases_path, columns, statuses):
        self.test_cases_path = test_cases_path
        self.columns = columns
        self.statuses = statuses
        self.retry_ref = []
        self.rows = []
        self.found_tests_amount = 0

    def get_rows(self):
        # Add header row
        header = []
        for column in self.columns:
            header.append(column['name'])
        self.rows.append(header)

        # Iterate through given path
        for file in self.test_cases_path.iterdir():
            if not file.is_dir():
                # Open file and load json data object
                try:
                    f = open(file)
                except UnicodeDecodeError:
                    f = open(file, encoding='utf8')

                data = json.load(f)

                # Get row
                row = self.get_row(data)

                # Continue loop if row is empty, otherwise, add row, to final list of rows
                if not row:
                    continue
                else:
                    self.rows.append(row)

        # Validate failed tests found
        self.found_tests_amount = len(self.rows) - 1  # All rows without header line
        if not self.found_tests_amount:
            print('No tests with ' + str(self.statuses) + ' status(-es) found!')
            exit()

        return self.rows

    def get_row(self, data):
        row = []
        # Get STATUS and TEST name
        status = self.get_status(data)
        test_name = self.get_full_name(data)

        # Remove test from final rows, if a current test is newer(was retried in test run)
        if self.is_test_already_present(test_name):
            if self.is_existing_test_is_older(test_name, data):
                self.remove_existing(test_name)
            else:
                return row

        # If status is passed return empty row
        if status in self.statuses:
            for column in self.columns:
                # Add empty row
                if not column['reportValue']:
                    row.append('')

                # Add 'name' to row array
                if column['reportValue'] == 'name':
                    name = self.get_name(data)
                    row.append(name)

                # Add 'fullName' name to row array
                if column['reportValue'] == 'fullName':
                    row.append(test_name)

                # Add 'package' name to row array
                if column['reportValue'] == 'package':
                    package = self.get_package(data)
                    row.append(package)

                # Add 'epic' name to row array
                if column['reportValue'] == 'epic':
                    epic = self.get_epic(data)
                    row.append(epic)

                # Add 'feature' name to row array
                if column['reportValue'] == 'feature':
                    epic = self.get_feature(data)
                    row.append(epic)

                # Add 'story' name to row array
                if column['reportValue'] == 'story':
                    epic = self.get_story(data)
                    row.append(epic)

                # Get 'shortMessage' and add to row array
                if column['reportValue'] == 'shortMessage':
                    message = self.get_message(data).partition('\n')[0]
                    row.append(message)

                # Get 'message' and add to row array
                if column['reportValue'] == 'message':
                    message = self.get_message(data)
                    row.append(message)

                # Get 'stepFailed' and add to row array
                if column['reportValue'] == 'stepFailed':
                    step = self.get_step_failed(data)
                    row.append(step)

                # Get 'category' and add to row array
                if column['reportValue'] == 'category':
                    category = self.get_category(data)
                    row.append(category)

                # Get 'durationMs' and add to row array
                if column['reportValue'] == 'durationMs':
                    duration = self.get_duration(data)
                    row.append(duration)

                # Get 'durationSec' and add to row array
                if column['reportValue'] == 'durationSec':
                    duration = self.get_duration(data) / 1000
                    row.append(duration)

                # Get 'durationMin' and add to row array
                if column['reportValue'] == 'durationMin':
                    duration = self.get_duration(data) / 1000 / 60
                    row.append(duration)

                # Get 'durationHrs' and add to row array
                if column['reportValue'] == 'durationHrs':
                    duration = self.get_duration(data) / 1000 / 60 / 60
                    row.append(duration)

                # Add 'status' to row array
                if column['reportValue'] == 'status':
                    row.append(status)

        # Collect test name and stop time
        self.collect_retry_ref(data)
        return row

    def collect_retry_ref(self, data):
        name = self.get_full_name(data)
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
    def get_name(data):
        try:
            return data['name']
        except KeyError:
            return ''

    @staticmethod
    def get_full_name(data):
        try:
            return data['fullName']
        except KeyError:
            return ''

    @staticmethod
    def get_package(data):
        try:
            for label in data['labels']:
                if label['name'] == 'package':
                    return label['value']
        except KeyError:
            return ''
        return ''

    @staticmethod
    def get_epic(data):
        epic = ''
        try:
            for label in data['labels']:
                if label['name'] == 'epic':
                    if epic == '':
                        epic = label['value']
                    else:
                        epic += '\n' + label['value']
        except KeyError:
            return epic
        return epic

    @staticmethod
    def get_feature(data):
        epic = ''
        try:
            for label in data['labels']:
                if label['name'] == 'feature':
                    if epic == '':
                        epic = label['value']
                    else:
                        epic += '\n' + label['value']
        except KeyError:
            return epic
        return epic

    @staticmethod
    def get_story(data):
        epic = ''
        try:
            for label in data['labels']:
                if label['name'] == 'story':
                    if epic == '':
                        epic = label['value']
                    else:
                        epic += '\n' + label['value']
        except KeyError:
            return epic
        return epic

    @staticmethod
    def get_message(data):
        try:
            return data['statusMessage']
        except KeyError:
            return ''

    @staticmethod
    def get_step_failed(data):
        try:
            for step in data['testStage']['steps']:
                if step['status'] == 'failed':
                    return step['name']
        except KeyError:
            return ''

    @staticmethod
    def get_duration(data):
        try:
            return data['time']['duration']
        except KeyError:
            return ''

    @staticmethod
    def get_category(data):
        try:
            categories = data['extra']['categories']
        except KeyError:
            categories = []
        multiple_categories = []

        if len(categories) == 0:
            return ''
        elif len(categories) == 1:
            return categories[0]['name']
        elif len(categories) == 2:
            for category in categories:
                if 'messageRegex' in category:
                    return category['name']
        else:
            for category in categories:
                if 'messageRegex' in category:
                    multiple_categories.append(category['name'])

        if len(multiple_categories) == 0:
            return ''
        else:
            return str(multiple_categories)

    @staticmethod
    def get_status(data):
        try:
            return data['status']
        except KeyError:
            return ''

    @staticmethod
    def get_stop_time(data):
        try:
            return data['time']['stop']
        except KeyError:
            return ''
