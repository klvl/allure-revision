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
        'name': 'NEW FAILED',
        'reportValue': 'newFailed'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'NEW FAILED'],
    ['io.klvl.AttachmentTest.testSimpleAttach', False],
    ['io.klvl.BrokenTest.testBroken', False],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', False],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', False],
    ['io.klvl.CategoriesTest.testSimpleCategory', False],
    ['io.klvl.DescriptionTest.testDescription', False],
    ['io.klvl.FlakyTest.testFlakyBroken', False],
    ['io.klvl.FlakyTest.testFlakyFailed', True],
    ['io.klvl.FlakyTest.testFlakyPassed', False],
    ['io.klvl.IssueTest.testIssue', False],
    ['io.klvl.IssueTest.testIssues', False],
    ['io.klvl.LinkTest.testLink', False],
    ['io.klvl.LinkTest.testNamedLink', False],
    ['io.klvl.ParametersTest.testParameters', False],
    ['io.klvl.RetryTest.testRetry1', False],
    ['io.klvl.RetryTest.testRetry2', False],
    ['io.klvl.RetryTest.testRetry3', False],
    ['io.klvl.RetryTest.testRetryMoreRetries', False],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', False],
    ['io.klvl.SimpleTest.testDescriptiveTestName', False],
    ['io.klvl.SimpleTest.testSimple', False],
    ['io.klvl.SkippedTest.testSkippedFirst', False],
    ['io.klvl.SkippedTest.testSkippedSecond', False],
    ['io.klvl.StepTest.testStepAsLambda', False],
    ['io.klvl.TmsLinkTest.testTmsLink', False]
]


def test_new_failed():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

