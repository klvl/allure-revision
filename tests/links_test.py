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
        'name': 'LINK(s)',
        'reportValue': 'link'
    }
]

STATUSES = ['failed', 'broken', 'passed', 'skipped', 'unknown']

EXPECTED_ROWS = [
    ['FULL NAME', 'LINK(s)'],
    ['io.klvl.AttachmentTest.testSimpleAttach', ''],
    ['io.klvl.BrokenTest.testBroken', ''],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', ''],
    ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', ''],
    ['io.klvl.CategoriesTest.testSimpleCategory', ''],
    ['io.klvl.DescriptionTest.testDescription', ''],
    ['io.klvl.IssueTest.testIssue', '=HYPERLINK("https://atlassian.jira.com/issue/KLVL-123", "KLVL-123")'],
    ['io.klvl.IssueTest.testIssues',
     'https://atlassian.jira.com/issue/KLVL-123\nhttps://atlassian.jira.com/issue/KLVL-124'],
    ['io.klvl.LinkTest.testLink', ''],
    ['io.klvl.LinkTest.testNamedLink', '=HYPERLINK("https://google.com", "google")'],
    ['io.klvl.ParametersTest.testParameters', ''],
    ['io.klvl.RetryTest.testRetry1', ''],
    ['io.klvl.RetryTest.testRetry2', ''],
    ['io.klvl.RetryTest.testRetry3', ''],
    ['io.klvl.SimpleTest.testDescriptiveTestName', ''],
    ['io.klvl.SimpleTest.testSimple', ''],
    ['io.klvl.SkippedTest.testSkippedFirst', ''],
    ['io.klvl.SkippedTest.testSkippedSecond', ''],
    ['io.klvl.StepTest.testStepAsLambda', ''],
    ['io.klvl.TmsLinkTest.testTmsLink', '=HYPERLINK("https://atlassian.jira.com/KLVL-123", "KLVL-123")']
]


def test_links():
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == EXPECTED_ROWS

