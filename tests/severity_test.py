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
        'name': 'SEVERITY',
        'reportValue': 'severity'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'SEVERITY'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'critical'],
    ['io.klvl.BrokenTest.testBroken', 'minor'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'normal'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'normal'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'normal'],
    ['io.klvl.DescriptionTest.testDescription', 'critical'],
    ['io.klvl.FlakyTest.testFlakyBroken', ''],
    ['io.klvl.FlakyTest.testFlakyFailed', ''],
    ['io.klvl.FlakyTest.testFlakyPassed', ''],
    ['io.klvl.IssueTest.testIssue', 'minor'],
    ['io.klvl.IssueTest.testIssues', 'trivial'],
    ['io.klvl.LinkTest.testLink', 'trivial'],
    ['io.klvl.LinkTest.testNamedLink', 'normal'],
    ['io.klvl.ParametersTest.testParameters', 'critical'],
    ['io.klvl.RetryTest.testRetry1', 'blocker'],
    ['io.klvl.RetryTest.testRetry2', 'critical'],
    ['io.klvl.RetryTest.testRetry3', 'normal'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'normal'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'normal'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', ''],
    ['io.klvl.SimpleTest.testSimple', 'trivial'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'blocker'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'critical'],
    ['io.klvl.StepTest.testStepAsLambda', 'blocker'],
    ['io.klvl.TmsLinkTest.testTmsLink', '']
]


def test_severity():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

