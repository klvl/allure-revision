import os
import pathlib

from main.report import ReportParser


def get_test_cases_dir():
    absolute_path = os.path.dirname(__file__)
    relative_path = "allure-report/data/test-cases"
    return pathlib.Path(os.path.join(absolute_path, relative_path))


TEST_CASES_PATH = get_test_cases_dir()

COLUMNS = [
    {
        'name': 'TEST',
        'reportValue': 'fullName'
    },
    {
        'name': 'STEP FAILED',
        'reportValue': 'stepFailed'
    }
]

STATUSES = ['failed']

EXPECTED_ROWS = [
    ['TEST', 'STEP FAILED'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'failStepD'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'failStepE'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'failStepC'],
    ['io.klvl.FlakyTest.testFlakyFailed', ''],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', '']
]


def test_step_failed():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

