import json

from sys import exit


class ReportParser:
    def __init__(self, test_cases_path, columns, statuses):
        self.test_cases_path = test_cases_path
        self.columns = columns
        self.statuses = statuses
        self.rows = []
        self.final_test_ids = self.collect_final_test_ids()
        self.found_tests_amount = 0

    def collect_final_test_ids(self):
        final_test_ids = []
        # Get last run uid(s)
        for file in self.test_cases_path.iterdir():
            if not file.is_dir():
                # Open file and load json data object
                try:
                    f = open(file)
                except UnicodeDecodeError:
                    f = open(file, encoding='utf8')

                data = json.load(f)

                # Get full_name, uid and stop_time
                current_full_name = self.get_full_name(data)
                current_uid = self.get_uid(data)
                current_stop_time = self.get_stop_time(data)

                # Get existing uid and stop_time
                existing_test_data = [item for item in final_test_ids if item['full_name'] == current_full_name]
                existing_test_uid = existing_test_data[0]['uid'] if len(existing_test_data) == 1 else None
                existing_test_stop_time = existing_test_data[0]['stop_time'] if len(existing_test_data) == 1 else None

                if existing_test_uid is None:  # if this test name is not present in final_test_ids just add it
                    final_test_ids.append({
                        'full_name': current_full_name,
                        'uid': current_uid,
                        'stop_time': current_stop_time
                    })
                else:  # if this test name is present in final_test_ids
                    if existing_test_stop_time > current_stop_time:
                        continue
                    else:
                        for item in final_test_ids:
                            if item['full_name'] == current_full_name:
                                item['uid'] = current_uid
                                item['stop_time'] = current_stop_time
                            else:
                                pass
        return final_test_ids

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

                # Check if the file is final retry
                uid = self.get_uid(data)
                if len([item for item in self.final_test_ids if item['uid'] == uid]) == 1:  # if is in final_ids
                    # Get row
                    row = self.get_row(data)

                    # Continue loop if row is empty, otherwise, add row, to final list of rows
                    if not row:
                        continue
                    else:
                        self.rows.append(row)
                else:
                    pass

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

        # If status is passed return empty row
        if status in self.statuses:
            for column in self.columns:
                # Add empty row
                if not column['reportValue']:
                    row.append('')

                # Add 'package' name to row array
                if column['reportValue'] == 'package':
                    package = self.get_package(data)
                    row.append(package)

                # Add 'name' to row array
                if column['reportValue'] == 'name':
                    name = self.get_name(data)
                    row.append(name)

                # Add 'fullName' name to row array
                if column['reportValue'] == 'fullName':
                    full_name = self.get_full_name(data)
                    row.append(full_name)

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

                # Add 'suite' name to row array
                if column['reportValue'] == 'suite':
                    epic = self.get_suite(data)
                    row.append(epic)

                # Get 'message' and add to row array
                if column['reportValue'] == 'message':
                    message = self.get_message(data)
                    row.append(message)

                # Get 'shortMessage' and add to row array
                if column['reportValue'] == 'shortMessage':
                    message = self.get_message(data).partition('\n')[0]
                    row.append(message)

                # Get 'stepFailed' and add to row array
                if column['reportValue'] == 'stepFailed':
                    step = self.get_step_failed(data)
                    row.append(step)

                # Get 'category' and add to row array
                if column['reportValue'] == 'category':
                    category = self.get_category(data)
                    row.append(category)

                # Add 'status' to row array
                if column['reportValue'] == 'status':
                    row.append(status)

                # Get 'severity' and add to row array
                if column['reportValue'] == 'severity':
                    severity = self.get_severity(data)
                    row.append(severity)

                # Get 'retry' and add to row array
                if column['reportValue'] == 'retry':
                    retry = self.get_retry(data)
                    row.append(retry)

                # Get 'retry' and add to row array
                if column['reportValue'] == 'retriesCount':
                    retries_count = self.get_retries_count(data)
                    row.append(retries_count)

                # Get 'links' and add to row array
                if column['reportValue'] == 'link':
                    links = self.get_links(data)
                    row.append(links)

                # Get 'flaky' and add to row array
                if column['reportValue'] == 'flaky':
                    flaky = self.get_flaky(data)
                    row.append(flaky)

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
        return row

    def get_report_values(self):
        report_values = []
        for column in self.columns:
            try:
                report_values.append(column['reportValue'])
            except KeyError:
                pass
        return report_values

    @staticmethod
    def get_uid(data):
        try:
            return data['uid']
        except KeyError:
            return ''

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
        feature = ''
        try:
            for label in data['labels']:
                if label['name'] == 'feature':
                    if feature == '':
                        feature = label['value']
                    else:
                        feature += '\n' + label['value']
        except KeyError:
            return feature
        return feature

    @staticmethod
    def get_story(data):
        story = ''
        try:
            for label in data['labels']:
                if label['name'] == 'story':
                    if story == '':
                        story = label['value']
                    else:
                        story += '\n' + label['value']
        except KeyError:
            return story
        return story

    @staticmethod
    def get_suite(data):
        suite = ''
        try:
            for label in data['labels']:
                if label['name'] == 'suite':
                    if suite == '':
                        suite = label['value']
                    else:
                        suite += '\n' + label['value']
        except KeyError:
            return suite
        return suite

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
    def get_severity(data):
        try:
            for label in data['labels']:
                if label['name'] == 'severity':
                    return label['value']
        except KeyError:
            return ''
        return ''

    @staticmethod
    def get_retries_count(data):
        try:
            return data['retriesCount']
        except KeyError:
            return ''

    def get_retry(self, data):
        retries_count = self.get_retries_count(data)
        if retries_count > 0:
            return '=TRUE'
        else:
            return '=FALSE'

    @staticmethod
    def get_links(data):
        try:
            links = data['links']
            if len(links) == 1:
                return '=HYPERLINK("' + links[0]['url'] + '", "' + links[0]['name'] + '")'
            else:
                report_links = ''
                for link in links:
                    if report_links == '':
                        report_links = link['url']
                    else:
                        report_links += '\n' + link['url']
                return report_links
        except KeyError:
            return ''

    @staticmethod
    def get_flaky(data):
        try:
            if data['flaky']:
                return '=TRUE'
            else:
                return '=FALSE'
        except KeyError:
            return '=FALSE'

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

    def get_test_name_key_retry_ref(self):
        for column in self.columns:
            try:
                if column['reportValue'] == 'fullName':
                    return 'fullName'
                elif column['reportValue'] == 'name':
                    return 'name'
            except KeyError:
                pass

    def get_test_name_by_retry_key(self, data):
        try:
            return data[self.test_name_key_retry_ref]
        except KeyError:
            return ''

    def get_test_name_column_index_retry_ref(self):
        for i, column in enumerate(self.columns):
            try:
                if column['reportValue'] == self.test_name_key_retry_ref:
                    return i
            except KeyError:
                pass

    def get_retry_column_index(self):
        for i, column in enumerate(self.columns):
            try:
                if column['reportValue'] == 'retry':
                    return i
            except KeyError:
                pass

    def collect_retry_ref(self, data):
        name = self.get_full_name(data)
        stop = self.get_stop_time(data)
        self.retry_ref.append({'name': name, 'stop_time': stop})

    def get_ref_stop_time(self, test_name_for_retry):
        for ref in self.retry_ref:
            if ref['name'] == test_name_for_retry:
                return ref['stop_time']

    def is_test_already_present(self, test_name_for_retry):
        for row in self.retry_ref:
            try:
                if row['name'] == test_name_for_retry:
                    return True
            except KeyError:
                pass
        return False

    def is_existing_test_is_older(self, test_name_for_retry, data):
        ref_stop = self.get_ref_stop_time(test_name_for_retry)
        actual_stop = self.get_stop_time(data)
        return ref_stop < actual_stop

    def remove_existing_test_from_rows(self, test_name_for_retry):
        for row in self.rows:
            if row[self.test_name_column_index_retry_ref] == test_name_for_retry:
                self.rows.remove(row)

    def set_retried_tests(self):
        retry_column_index = self.get_retry_column_index()

        for i, row in enumerate(self.rows):
            if i == 0:  # Skip a header line
                continue
            else:
                for m, column in enumerate(row):
                    if m == retry_column_index:
                        if row[self.test_name_column_index_retry_ref] in self.retried_tests:
                            row[m] = '=TRUE'
                        else:
                            row[m] = '=FALSE'
