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
        'name': 'RETRIES COUNT',
        'reportValue': 'retriesCount'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'RETRIES COUNT'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 0],
    ['io.klvl.BrokenTest.testBroken', 0],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 0],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 0],
    ['io.klvl.CategoriesTest.testSimpleCategory', 0],
    ['io.klvl.DescriptionTest.testDescription', 0],
    ['io.klvl.FlakyTest.testFlakyBroken', 0],
    ['io.klvl.FlakyTest.testFlakyFailed', 0],
    ['io.klvl.FlakyTest.testFlakyPassed', 0],
    ['io.klvl.IssueTest.testIssue', 0],
    ['io.klvl.IssueTest.testIssues', 0],
    ['io.klvl.LinkTest.testLink', 0],
    ['io.klvl.LinkTest.testNamedLink', 0],
    ['io.klvl.ParametersTest.testParameters', 0],
    ['io.klvl.RetryTest.testRetry1', 1],
    ['io.klvl.RetryTest.testRetry2', 1],
    ['io.klvl.RetryTest.testRetry3', 1],
    ['io.klvl.RetryTest.testRetryMoreRetries', 4],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 1],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 0],
    ['io.klvl.SimpleTest.testSimple', 0],
    ['io.klvl.SkippedTest.testSkippedFirst', 0],
    ['io.klvl.SkippedTest.testSkippedSecond', 0],
    ['io.klvl.StepTest.testStepAsLambda', 0],
    ['io.klvl.TmsLinkTest.testTmsLink', 0]
]


def test_retries_count():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

