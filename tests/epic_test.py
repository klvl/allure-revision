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
        'name': 'EPIC',
        'reportValue': 'epic'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'EPIC'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'Allure revision\nExtra epic'],
    ['io.klvl.BrokenTest.testBroken', 'Allure revision'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'Allure revision'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'Allure revision'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'Allure revision'],
    ['io.klvl.DescriptionTest.testDescription', 'Allure revision'],
    ['io.klvl.FlakyTest.testFlakyBroken', ''],
    ['io.klvl.FlakyTest.testFlakyFailed', ''],
    ['io.klvl.FlakyTest.testFlakyPassed', ''],
    ['io.klvl.IssueTest.testIssue', 'Allure revision'],
    ['io.klvl.IssueTest.testIssues', 'Allure revision'],
    ['io.klvl.LinkTest.testLink', 'Allure revision'],
    ['io.klvl.LinkTest.testNamedLink', 'Allure revision'],
    ['io.klvl.ParametersTest.testParameters', 'Allure revision'],
    ['io.klvl.RetryTest.testRetry1', 'Allure revision'],
    ['io.klvl.RetryTest.testRetry2', 'Allure revision'],
    ['io.klvl.RetryTest.testRetry3', 'Allure revision'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'Allure revision'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'Allure revision'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'Allure revision'],
    ['io.klvl.SimpleTest.testSimple', 'Allure revision'],
    ['io.klvl.SkippedTest.testSkippedFirst', ''],
    ['io.klvl.SkippedTest.testSkippedSecond', ''],
    ['io.klvl.StepTest.testStepAsLambda', 'Allure revision'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'Allure revision']
]


def test_epic():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

