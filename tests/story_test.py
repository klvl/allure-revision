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
        'name': 'STORY',
        'reportValue': 'story'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'STORY'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'As a user I can attach file'],
    ['io.klvl.BrokenTest.testBroken', 'Broken test'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'As a user I can see defect category\nExtra story'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'As a user I can see defect category\nExtra story'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'As a user I can see defect category\nExtra story'],
    ['io.klvl.DescriptionTest.testDescription', 'As a user I can see test description'],
    ['io.klvl.FlakyTest.testFlakyBroken', ''],
    ['io.klvl.FlakyTest.testFlakyFailed', ''],
    ['io.klvl.FlakyTest.testFlakyPassed', ''],
    ['io.klvl.IssueTest.testIssue', 'As a user I can see issue link'],
    ['io.klvl.IssueTest.testIssues', 'As a user I can see issue link'],
    ['io.klvl.LinkTest.testLink', 'As a user I can see normal link'],
    ['io.klvl.LinkTest.testNamedLink', 'As a user I can see normal link'],
    ['io.klvl.ParametersTest.testParameters', 'As a user I can see test parameters'],
    ['io.klvl.RetryTest.testRetry1', 'As a user I can see retried test'],
    ['io.klvl.RetryTest.testRetry2', 'As a user I can see retried test'],
    ['io.klvl.RetryTest.testRetry3', 'As a user I can see retried test'],
    ['io.klvl.RetryTest.testRetryMoreRetries', 'As a user I can see retried test'],
    ['io.klvl.RetryTest.testRetryStatusNotChangedAfterRetry', 'As a user I can see retried test'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', ''],
    ['io.klvl.SimpleTest.testSimple', ''],
    ['io.klvl.SkippedTest.testSkippedFirst', 'As a user I can see skipped test'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'As a user I can see skipped test'],
    ['io.klvl.StepTest.testStepAsLambda', 'As a use I can see steps in the test'],
    ['io.klvl.TmsLinkTest.testTmsLink', 'As a user I can see TMS link']
]


def test_story():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

