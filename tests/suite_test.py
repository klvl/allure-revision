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
        'name': 'SUITE',
        'reportValue': 'suite'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'SUITE'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'Regression test'],
    ['io.klvl.BrokenTest.testBroken', 'Regression test'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'Regression test'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'Regression test'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'Regression test'],
    ['io.klvl.DescriptionTest.testDescription', 'Regression test\nExtra suite'],
    ['io.klvl.FlakyTest.testFlakyBroken', 'Regression test'],
    ['io.klvl.FlakyTest.testFlakyFailed', 'Regression test'],
    ['io.klvl.FlakyTest.testFlakyPassed', 'Regression test'],
    ['io.klvl.IssueTest.testIssue', 'Regression test'],
    ['io.klvl.IssueTest.testIssues', 'Regression test'],
    ['io.klvl.LinkTest.testLink', 'Regression test'],
    ['io.klvl.LinkTest.testNamedLink', 'Regression test'],
    ['io.klvl.ParametersTest.testParameters', 'Regression test'],
    ['io.klvl.RetryTest.testRetry1', 'Regression test'],
    ['io.klvl.RetryTest.testRetry2', 'Regression test'],
    ['io.klvl.RetryTest.testRetry3', 'Regression test'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'Regression test'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'Regression test'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'Regression test'],
    ['io.klvl.SimpleTest.testSimple', 'Regression test'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'Regression test'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'Regression test'],
    ['io.klvl.StepTest.testStepAsLambda', 'Regression test'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'Regression test']
]


def test_suite():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

