import os
import pathlib
import pytest

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
        'name': 'PACKAGE',
        'reportValue': 'package'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'PACKAGE'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'io.klvl.AttachmentTest'],
    ['io.klvl.BrokenTest.testBroken', 'io.klvl.BrokenTest'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'io.klvl.CategoriesTest'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'io.klvl.CategoriesTest'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'io.klvl.CategoriesTest'],
    ['io.klvl.DescriptionTest.testDescription', 'io.klvl.DescriptionTest'],
    ['io.klvl.FlakyTest.testFlakyBroken', 'io.klvl.FlakyTest'],
    ['io.klvl.FlakyTest.testFlakyFailed', 'io.klvl.FlakyTest'],
    ['io.klvl.FlakyTest.testFlakyPassed', 'io.klvl.FlakyTest'],
    ['io.klvl.IssueTest.testIssue', 'io.klvl.IssueTest'],
    ['io.klvl.IssueTest.testIssues', 'io.klvl.IssueTest'],
    ['io.klvl.LinkTest.testLink', 'io.klvl.LinkTest'],
    ['io.klvl.LinkTest.testNamedLink', 'io.klvl.LinkTest'],
    ['io.klvl.ParametersTest.testParameters', 'io.klvl.ParametersTest'],
    ['io.klvl.RetryTest.testRetry1', 'io.klvl.RetryTest'],
    ['io.klvl.RetryTest.testRetry2', 'io.klvl.RetryTest'],
    ['io.klvl.RetryTest.testRetry3', 'io.klvl.RetryTest'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'io.klvl.RetryTest'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'io.klvl.RetryTest'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'io.klvl.SimpleTest'],
    ['io.klvl.SimpleTest.testSimple', 'io.klvl.SimpleTest'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'io.klvl.SkippedTest'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'io.klvl.SkippedTest'],
    ['io.klvl.StepTest.testStepAsLambda', 'io.klvl.StepTest'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'io.klvl.TmsLinkTest']
]


def test_package():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

