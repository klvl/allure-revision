from __future__ import print_function

from arguments import ArgumentsParser
from report import ReportParser
from spreadsheet import SpreadsheetActions
from config import ConfigParser


def main():
    # Parse arguments
    args = ArgumentsParser()
    config = ConfigParser(args.config_path)

    # Parse failed tests
    report = ReportParser(args.test_cases_path, config)
    rows = report.get_rows()

    # Initialize service, create new sheet, upload rows
    spreadsheet = SpreadsheetActions(config, args.sheet_name, rows)
    spreadsheet.create_sheet()
    spreadsheet.upload_rows()

    # Collect requests

    # Collect change column sizes requests
    spreadsheet.collect_update_column_size_rq(0, 700)
    spreadsheet.collect_update_column_size_rq(1, 250)
    spreadsheet.collect_update_column_size_rq(2, 200)
    spreadsheet.collect_update_column_size_rq(3, 80)
    spreadsheet.collect_update_column_size_rq(4, 80)
    spreadsheet.collect_update_column_size_rq(5, 300)

    # Collect sort columns request
    spreadsheet.collect_sort_rq(1, 0, 'ASCENDING', 0)

    # Collect freeze header column request
    spreadsheet.collect_freeze_rows_rq(1)

    # Set conditional formatting
    spreadsheet.collect_conditional_formatting_to_all_rows('=EQ(D2, "failed")', 'light_red')
    spreadsheet.collect_conditional_formatting_to_all_rows('=EQ(D2, "broken")', 'yellow')
    spreadsheet.collect_conditional_formatting_to_all_rows('=EQ(E2, "fixed")', 'green')
    spreadsheet.collect_conditional_formatting_to_all_rows('=EQ(E2, "passed")', 'green')
    spreadsheet.collect_conditional_formatting_to_all_rows('=EQ(E2, "bug")', 'dark_red')
    spreadsheet.execute_requests()

    # Print successful result message
    print('Uploaded on "' + args.sheet_name + '" sheet: ' + spreadsheet.get_link_to_sheet())


if __name__ == '__main__':
    main()
