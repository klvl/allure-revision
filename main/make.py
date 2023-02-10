from __future__ import print_function

from arguments import ArgumentsParser
from config import ConfigParser
from report import ReportParser
from spreadsheet import SpreadsheetActions


def main():
    # Parse arguments
    args = ArgumentsParser()
    config = ConfigParser(args.config_path, args.spreadsheet_id, args.token)

    # Parse failed tests
    report = ReportParser(args.test_cases_path, config)

    # Initialize spreadsheet service
    spreadsheet = SpreadsheetActions(config, args.sheet_name, report.rows)

    # Create new sheet and upload rows
    spreadsheet.create_sheet()
    spreadsheet.upload_rows()

    # Collect requests
    spreadsheet.collect_move_sheet_to_index_request()
    spreadsheet.collect_update_column_size_requests()
    spreadsheet.collect_sort_request()
    spreadsheet.collect_freeze_rows_request()
    spreadsheet.collect_conditional_formatting_to_all_rows()

    # Execute requests
    spreadsheet.execute_requests()

    # Print successful result message
    print('\nUploaded ' + str(report.found_tests_amount) + ' tests with ' + str(config.statuses) + ' status(-es) ' +
          'on the "' + args.sheet_name + '" sheet:\n' + spreadsheet.get_link_to_sheet())


if __name__ == '__main__':
    main()
