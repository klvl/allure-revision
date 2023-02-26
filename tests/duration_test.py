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
        ['io.klvl.AttachmentTest.testSimpleAttach', 10],
        ['io.klvl.BrokenTest.testBroken', 1],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 1],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 1],
        ['io.klvl.CategoriesTest.testSimpleCategory', 1],
        ['io.klvl.DescriptionTest.testDescription', 1],
        ['io.klvl.IssueTest.testIssue', 2],
        ['io.klvl.IssueTest.testIssues', 0],
        ['io.klvl.LinkTest.testLink', 1],
        ['io.klvl.LinkTest.testNamedLink', 0],
        ['io.klvl.ParametersTest.testParameters', 2],
        ['io.klvl.RetryTest.testRetry1', 1],
        ['io.klvl.RetryTest.testRetry2', 1],
        ['io.klvl.RetryTest.testRetry3', 0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 0],
        ['io.klvl.SimpleTest.testSimple', 0],
        ['io.klvl.SkippedTest.testSkippedFirst', 1],
        ['io.klvl.SkippedTest.testSkippedSecond', 0],
        ['io.klvl.StepTest.testStepAsLambda', 21],
        ['io.klvl.TmsLinkTest.testTmsLink', 1]
    ],
    [
        ['TEST', 'DURATION(sec)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 0.01],
        ['io.klvl.BrokenTest.testBroken', 0.001],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 0.001],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 0.001],
        ['io.klvl.CategoriesTest.testSimpleCategory', 0.001],
        ['io.klvl.DescriptionTest.testDescription', 0.001],
        ['io.klvl.IssueTest.testIssue', 0.002],
        ['io.klvl.IssueTest.testIssues', 0.0],
        ['io.klvl.LinkTest.testLink', 0.001],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 0.002],
        ['io.klvl.RetryTest.testRetry1', 0.001],
        ['io.klvl.RetryTest.testRetry2', 0.001],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 0.0],
        ['io.klvl.SimpleTest.testSimple', 0.0],
        ['io.klvl.SkippedTest.testSkippedFirst', 0.001],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 0.021],
        ['io.klvl.TmsLinkTest.testTmsLink', 0.001]
    ],
    [
        ['TEST', 'DURATION(min)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 0.00016666666666666666],
        ['io.klvl.BrokenTest.testBroken', 1.6666666666666667e-05],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 1.6666666666666667e-05],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 1.6666666666666667e-05],
        ['io.klvl.CategoriesTest.testSimpleCategory', 1.6666666666666667e-05],
        ['io.klvl.DescriptionTest.testDescription', 1.6666666666666667e-05],
        ['io.klvl.IssueTest.testIssue', 3.3333333333333335e-05],
        ['io.klvl.IssueTest.testIssues', 0.0],
        ['io.klvl.LinkTest.testLink', 1.6666666666666667e-05],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 3.3333333333333335e-05],
        ['io.klvl.RetryTest.testRetry1', 1.6666666666666667e-05],
        ['io.klvl.RetryTest.testRetry2', 1.6666666666666667e-05],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 0.0],
        ['io.klvl.SimpleTest.testSimple', 0.0],
        ['io.klvl.SkippedTest.testSkippedFirst', 1.6666666666666667e-05],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 0.00035],
        ['io.klvl.TmsLinkTest.testTmsLink', 1.6666666666666667e-05]
    ],
    [
        ['TEST', 'DURATION(hrs)'],
        ['io.klvl.AttachmentTest.testSimpleAttach', 2.7777777777777775e-06],
        ['io.klvl.BrokenTest.testBroken', 2.777777777777778e-07],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 2.777777777777778e-07],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 2.777777777777778e-07],
        ['io.klvl.CategoriesTest.testSimpleCategory', 2.777777777777778e-07],
        ['io.klvl.DescriptionTest.testDescription', 2.777777777777778e-07],
        ['io.klvl.IssueTest.testIssue', 5.555555555555556e-07],
        ['io.klvl.IssueTest.testIssues', 0.0],
        ['io.klvl.LinkTest.testLink', 2.777777777777778e-07],
        ['io.klvl.LinkTest.testNamedLink', 0.0],
        ['io.klvl.ParametersTest.testParameters', 5.555555555555556e-07],
        ['io.klvl.RetryTest.testRetry1', 2.777777777777778e-07],
        ['io.klvl.RetryTest.testRetry2', 2.777777777777778e-07],
        ['io.klvl.RetryTest.testRetry3', 0.0],
        ['io.klvl.SimpleTest.testDescriptiveTestName', 0.0],
        ['io.klvl.SimpleTest.testSimple', 0.0],
        ['io.klvl.SkippedTest.testSkippedFirst', 2.777777777777778e-07],
        ['io.klvl.SkippedTest.testSkippedSecond', 0.0],
        ['io.klvl.StepTest.testStepAsLambda', 5.833333333333333e-06],
        ['io.klvl.TmsLinkTest.testTmsLink', 2.777777777777778e-07]
    ]
]


@pytest.mark.parametrize('columns, expected_rows', zip(COLUMNS, EXPECTED_ROWS))
def test_duration(columns, expected_rows):
    report_parser = ReportParser(TEST_CASES_PATH, columns, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == expected_rows

