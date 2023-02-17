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
            'name': 'STATUS',
            'reportValue': 'message'
        }
    ],
    [
        {
            'name': 'TEST',
            'reportValue': 'fullName'
        },
        {
            'name': 'STATUS',
            'reportValue': 'shortMessage'
        }
    ]
]

STATUSES = ['failed', 'skipped', 'broken']

EXPECTED_ROWS = [
    [
        ['TEST', 'STATUS'],
        ['io.klvl.BrokenTest.testBroken', 'Cannot invoke "String.isEmpty()" because "nullable" is null'],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp',
         'The status code did not match expected!\nTry to check logs!'],

        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2',
         'The status code did not match expected!\nTry to check logs!'],

        ['io.klvl.CategoriesTest.testSimpleCategory', 'null'],
        ['io.klvl.SkippedTest.testSkippedFirst', 'The first skipped!'],
        ['io.klvl.SkippedTest.testSkippedSecond', 'The second skipped!']
    ],
    [
        ['TEST', 'STATUS'],
        ['io.klvl.BrokenTest.testBroken', 'Cannot invoke "String.isEmpty()" because "nullable" is null'],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp', 'The status code did not match expected!'],
        ['io.klvl.CategoriesTest.testCategoryByMessageRegExp2', 'The status code did not match expected!'],
        ['io.klvl.CategoriesTest.testSimpleCategory', 'null'],
        ['io.klvl.SkippedTest.testSkippedFirst', 'The first skipped!'],
        ['io.klvl.SkippedTest.testSkippedSecond', 'The second skipped!']
    ]
]


@pytest.mark.parametrize('columns, expected_rows', zip(COLUMNS, EXPECTED_ROWS))
def test_message(columns, expected_rows):
    report_parser = ReportParser(TEST_CASES_PATH, columns, STATUSES)
    actual_rows = sorted(report_parser.get_rows())

    assert actual_rows == expected_rows

