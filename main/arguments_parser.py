import os
import sys
import pathlib


class ArgumentsParser:
    def __init__(self):
        if len(sys.argv) != 3:
            print(
                'Improper usage! Example:\n\npython3 make.py allure-report/ regression-1\n')
            exit()

        self.test_cases_dir = None
        self.init_test_cases_dir()

        self.build_id = None
        self.init_build_id()

    def init_test_cases_dir(self):
        report_path = sys.argv[1]
        path_length = len(report_path)
        last_char = report_path[path_length - 1]
        if last_char == '/':
            self.test_cases_dir = report_path + "data/test-cases/"
        else:
            self.test_cases_dir = report_path + "/data/test-cases/"

    def init_build_id(self):
        self.build_id = "#" + sys.argv[2]

    def get_report_path(self):
        print('Get allure-report path...')
        if not os.path.exists(self.test_cases_dir):
            print('The ' + self.test_cases_dir + ' directory does not exist!')
            exit()
        return pathlib.Path(self.test_cases_dir)

    def get_build_id(self):
        print('Get build_id...')
        return self.build_id
