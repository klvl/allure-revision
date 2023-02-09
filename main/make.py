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
    report = ReportParser(args.test_cases_path)
    rows = report.get_rows()

    # Get rows and columns length
    rows_length = len(rows)
    columns_length = len(report.header)

    # Initialize service, create new sheet, upload rows
    spreadsheet = SpreadsheetActions(config.spreadsheet_id, args.sheet_name)
    spreadsheet.create_sheet()
    spreadsheet.upload_rows(rows)

    # Collect requests

    # Collect delete extra rows and columns requests
    spreadsheet.collect_delete_extra_columns_rq(columns_length)
    spreadsheet.collect_delete_extra_rows_rq(rows_length)

    # Collect change column sizes requests
    spreadsheet.collect_update_column_size_rq(0, 700)
    spreadsheet.collect_update_column_size_rq(1, 250)
    spreadsheet.collect_update_column_size_rq(2, 200)
    spreadsheet.collect_update_column_size_rq(3, 80)
    spreadsheet.collect_update_column_size_rq(4, 80)
    spreadsheet.collect_update_column_size_rq(5, 300)

    # Collect sort columns request
    spreadsheet.collect_sort_rq(1, rows_length, 0, columns_length, 'ASCENDING', 0)

    # Collect freeze header column request
    spreadsheet.collect_freeze_rows_rq(1)

    # Set conditional formatting
    spreadsheet.collect_conditional_formatting_to_all_rows(columns_length, rows_length,
                                                           '=EQ(D2, "failed")', 'light_red')
    spreadsheet.collect_conditional_formatting_to_all_rows(columns_length, rows_length,
                                                           '=EQ(D2, "broken")', 'yellow')
    spreadsheet.collect_conditional_formatting_to_all_rows(columns_length, rows_length,
                                                           '=EQ(E2, "fixed")', 'green')
    spreadsheet.collect_conditional_formatting_to_all_rows(columns_length, rows_length,
                                                           '=EQ(E2, "passed")', 'green')
    spreadsheet.collect_conditional_formatting_to_all_rows(columns_length, rows_length,
                                                           '=EQ(E2, "bug")', 'dark_red')
    spreadsheet.execute_requests()

    # Print successful result message
    print('Aggregation was successful! Results:\n' + spreadsheet.get_link_to_sheet())


if __name__ == '__main__':
    main()
