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
        'name': 'TEST',
        'reportValue': 'fullName'
    },
    {
        'name': 'STATUS',
        'reportValue': 'status'
    }
]

STATUSES = [
    ['failed'],
    ['skipped'],
    ['broken'],
    ['unknown'],
    ['passed']
]

EXPECTED_ROWS = [
    [
        ['TEST', 'STATUS'],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'failed'],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'failed'],
        ['io.klvl.CategoriesTest.testSimpleCategory', 'failed']
    ],
    [
        ['TEST', 'STATUS'],
        ['io.klvl.SkippedTest.testSkippedFirst', 'skipped'],
        ['io.klvl.SkippedTest.testSkippedSecond', 'skipped']
    ],
    [
        ['TEST', 'STATUS'],
        ['io.klvl.BrokenTest.testBroken', 'broken']
    ],
    [
        ['TEST', 'STATUS'],
        ['io.klvl.IssueTest.testIssue', 'unknown'],
        ['io.klvl.IssueTest.testIssues', 'unknown']
    ],
    [
        ['TEST', 'STATUS'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 'passed'],
        ['io.klvl.DescriptionTest.testDescription', 'passed'],
        ['io.klvl.LinkTest.testLink', 'passed'],
        ['io.klvl.LinkTest.testNamedLink', 'passed'],
        ['io.klvl.ParametersTest.testParameters', 'passed'],
        ['io.klvl.RetryTest.testRetry1', 'passed'],
        ['io.klvl.RetryTest.testRetry2', 'passed'],
        ['io.klvl.RetryTest.testRetry3', 'passed'],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 'passed'],
        ['io.klvl.SimpleTest.testSimple', 'passed'],
        ['io.klvl.StepTest.testStepAsLambda', 'passed'],
        ['io.klvl.TmsLinkTest.testTmsLink', 'passed']
    ]
]


@pytest.mark.parametrize('statuses, expected_rows', zip(STATUSES, EXPECTED_ROWS))
def test_status(statuses, expected_rows):
    report_parser = ReportParser(TEST_CASES_PATH, COLUMNS, statuses)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == expected_rows

