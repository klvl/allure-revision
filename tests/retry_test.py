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
        'name': 'FULL NAME',
        'reportValue': 'fullName'
    },
    {
        'name': 'WAS RETRIED',
        'reportValue': 'retry'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'WAS RETRIED'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'FALSE'],
    ['io.klvl.BrokenTest.testBroken', 'FALSE'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'FALSE'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'FALSE'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'FALSE'],
    ['io.klvl.DescriptionTest.testDescription', 'FALSE'],
    ['io.klvl.IssueTest.testIssue', 'FALSE'],
    ['io.klvl.IssueTest.testIssues', 'FALSE'],
    ['io.klvl.LinkTest.testLink', 'FALSE'],
    ['io.klvl.LinkTest.testNamedLink', 'FALSE'],
    ['io.klvl.ParametersTest.testParameters', 'FALSE'],
    ['io.klvl.RetryTest.testRetry1', 'TRUE'],
    ['io.klvl.RetryTest.testRetry2', 'TRUE'],
    ['io.klvl.RetryTest.testRetry3', 'TRUE'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'FALSE'],
    ['io.klvl.SimpleTest.testSimple', 'FALSE'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'FALSE'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'FALSE'],
    ['io.klvl.StepTest.testStepAsLambda', 'FALSE'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'FALSE']
]


def test_retry():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

