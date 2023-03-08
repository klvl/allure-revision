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
        'name': 'NAME',
        'reportValue': 'name'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'NAME'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'testSimpleAttach'],
    ['io.klvl.BrokenTest.testBroken', 'testBroken'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'testCategoryByMessageRegExp'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'testCategoryByMessageRegExp2'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'testSimpleCategory'],
    ['io.klvl.DescriptionTest.testDescription', 'testDescription'],
    ['io.klvl.FlakyTest.testFlakyBroken', 'testFlakyBroken'],
    ['io.klvl.FlakyTest.testFlakyFailed', 'testFlakyFailed'],
    ['io.klvl.FlakyTest.testFlakyPassed', 'testFlakyPassed'],
    ['io.klvl.IssueTest.testIssue', 'testIssue'],
    ['io.klvl.IssueTest.testIssues', 'testIssues'],
    ['io.klvl.LinkTest.testLink', 'testLink'],
    ['io.klvl.LinkTest.testNamedLink', 'testNamedLink'],
    ['io.klvl.ParametersTest.testParameters', 'testParameters'],
    ['io.klvl.RetryTest.testRetry1', 'testRetry1'],
    ['io.klvl.RetryTest.testRetry2', 'testRetry2'],
    ['io.klvl.RetryTest.testRetry3', 'testRetry3'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'testRetryMoreRetries'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'testRetryStatusNotChangedAfterRetry'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'As a user I see descriptive test name in a report'],
    ['io.klvl.SimpleTest.testSimple', 'testSimple'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'testSkippedFirst'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'testSkippedSecond'],
    ['io.klvl.StepTest.testStepAsLambda', 'testStepAsLambda'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'testTmsLink']
]


def test_name():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

