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
        'name': 'CATEGORY',
        'reportValue': 'category'
    }
]

STATUSES = ['failed', 'broken', 'unknown']

EXPECTED_ROWS = [
    ['TEST', 'CATEGORY'],
    ['io.klvl.BrokenTest.testBroken', 'Broken tests'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'Response status code mismatch'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'Response status code mismatch'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'All Failed Tests'],
    ['io.klvl.IssueTest.testIssue', 'Known issues'],
    ['io.klvl.IssueTest.testIssues', 'Known issues']
]


def test_category():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    print(actual_rows)

    assert actual_rows == EXPECTED_ROWS

