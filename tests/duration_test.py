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
    [
        {
            'name': 'TEST',
            'reportValue': 'fullName'
        },
        {
            'name': 'DURATION(ms)',
            'reportValue': 'durationMs'
        }
    ],
    [
        {
            'name': 'TEST',
            'reportValue': 'fullName'
        },
        {
            'name': 'DURATION(sec)',
            'reportValue': 'durationSec'
        }
    ],
    [
        {
            'name': 'TEST',
            'reportValue': 'fullName'
        },
        {
            'name': 'DURATION(min)',
            'reportValue': 'durationMin'
        }
    ],
    [
        {
            'name': 'TEST',
            'reportValue': 'fullName'
        },
        {
            'name': 'DURATION(hrs)',
            'reportValue': 'durationHrs'
        }
    ]
]

STATUSES = ['failed', 'skipped', 'broken', 'passed', 'unknown']

EXPECTED_ROWS = [
    [
        ['TEST', 'DURATION(ms)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 9],
        ['io.klvl.BrokenTest.testBroken', 2],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 1],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 2],
        ['io.klvl.CategoriesTest.testSimpleCategory', 1],
        ['io.klvl.DescriptionTest.testDescription', 1],
        ['io.klvl.IssueTest.testIssue', 0],
        ['io.klvl.IssueTest.testIssues', 2],
        ['io.klvl.LinkTest.testLink', 0],
        ['io.klvl.LinkTest.testNamedLink', 0],
        ['io.klvl.ParametersTest.testParameters', 2],
        ['io.klvl.RetryTest.testRetry1', 0],
        ['io.klvl.RetryTest.testRetry2', 0],
        ['io.klvl.RetryTest.testRetry3', 0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 1],
        ['io.klvl.SimpleTest.testSimple', 1],
        ['io.klvl.SkippedTest.testSkippedFirst', 0],
        ['io.klvl.SkippedTest.testSkippedSecond', 0],
        ['io.klvl.StepTest.testStepAsLambda', 19],
        ['io.klvl.TmsLinkTest.testTmsLink', 0]
    ],
    [
        ['TEST', 'DURATION(sec)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 0.009],
        ['io.klvl.BrokenTest.testBroken', 0.002],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 0.001],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 0.002],
        ['io.klvl.CategoriesTest.testSimpleCategory', 0.001],
        ['io.klvl.DescriptionTest.testDescription', 0.001],
        ['io.klvl.IssueTest.testIssue', 0.0],
        ['io.klvl.IssueTest.testIssues', 0.002],
        ['io.klvl.LinkTest.testLink', 0.0],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 0.002],
        ['io.klvl.RetryTest.testRetry1', 0.0],
        ['io.klvl.RetryTest.testRetry2', 0.0],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 0.001],
        ['io.klvl.SimpleTest.testSimple', 0.001],
        ['io.klvl.SkippedTest.testSkippedFirst', 0.0],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 0.019],
        ['io.klvl.TmsLinkTest.testTmsLink', 0.0]
    ],
    [
        ['TEST', 'DURATION(min)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 0.00015],
        ['io.klvl.BrokenTest.testBroken', 3.3333333333333335e-05],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 1.6666666666666667e-05],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 3.3333333333333335e-05],
        ['io.klvl.CategoriesTest.testSimpleCategory', 1.6666666666666667e-05],
        ['io.klvl.DescriptionTest.testDescription', 1.6666666666666667e-05],
        ['io.klvl.IssueTest.testIssue', 0.0],
        ['io.klvl.IssueTest.testIssues', 3.3333333333333335e-05],
        ['io.klvl.LinkTest.testLink', 0.0],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 3.3333333333333335e-05],
        ['io.klvl.RetryTest.testRetry1', 0.0],
        ['io.klvl.RetryTest.testRetry2', 0.0],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 1.6666666666666667e-05],
        ['io.klvl.SimpleTest.testSimple', 1.6666666666666667e-05],
        ['io.klvl.SkippedTest.testSkippedFirst', 0.0],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 0.00031666666666666665],
        ['io.klvl.TmsLinkTest.testTmsLink', 0.0]
    ],
    [
        ['TEST', 'DURATION(hrs)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 2.4999999999999998e-06],
        ['io.klvl.BrokenTest.testBroken', 5.555555555555556e-07],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 2.777777777777778e-07],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 5.555555555555556e-07],
        ['io.klvl.CategoriesTest.testSimpleCategory', 2.777777777777778e-07],
        ['io.klvl.DescriptionTest.testDescription', 2.777777777777778e-07],
        ['io.klvl.IssueTest.testIssue', 0.0],
        ['io.klvl.IssueTest.testIssues', 5.555555555555556e-07],
        ['io.klvl.LinkTest.testLink', 0.0],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 5.555555555555556e-07],
        ['io.klvl.RetryTest.testRetry1', 0.0],
        ['io.klvl.RetryTest.testRetry2', 0.0],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 2.777777777777778e-07],
        ['io.klvl.SimpleTest.testSimple', 2.777777777777778e-07],
        ['io.klvl.SkippedTest.testSkippedFirst', 0.0],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 5.277777777777778e-06],
        ['io.klvl.TmsLinkTest.testTmsLink', 0.0]
    ]
]


@pytest.mark.parametrize('columns, expected_rows', zip(COLUMNS, EXPECTED_ROWS))
def test_duration(columns, expected_rows):
    report_parser = ReportParser(TEST_CASES_PATH, columns, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == expected_rows

