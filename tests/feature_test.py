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
        'name': 'FEATURE',
        'reportValue': 'feature'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'FEATURE'],
    ['io.klvl.AttachmentTest.testSimpleAttach', 'Attachment'],
    ['io.klvl.BrokenTest.testBroken', 'Report statuses\nExtra feature'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'Categories'],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'Categories'],
    ['io.klvl.CategoriesTest.testSimpleCategory', 'Categories'],
    ['io.klvl.DescriptionTest.testDescription', 'Test description'],
    ['io.klvl.IssueTest.testIssue', 'Links'],
    ['io.klvl.IssueTest.testIssues', 'Links'],
    ['io.klvl.LinkTest.testLink', 'Links'],
    ['io.klvl.LinkTest.testNamedLink', 'Links'],
    ['io.klvl.ParametersTest.testParameters', 'Parameters'],
    ['io.klvl.RetryTest.testRetry1', 'Retry'],
    ['io.klvl.RetryTest.testRetry2', 'Retry'],
    ['io.klvl.RetryTest.testRetry3', 'Retry'],
    ['io.klvl.SimpleTest.testDescriptiveTestName', 'Simple'],
    ['io.klvl.SimpleTest.testSimple', 'Simple'],
    ['io.klvl.SkippedTest.testSkippedFirst', 'Report statuses'],
    ['io.klvl.SkippedTest.testSkippedSecond', 'Report statuses'],
    ['io.klvl.StepTest.testStepAsLambda', ''],
    ['io.klvl.TmsLinkTest.testTmsLink', 'Links']
]


def test_feature():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

