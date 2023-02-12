from __future__ import print_function

from data_provider import DataProvider
from report import ReportParser
from spreadsheet import SpreadsheetActions


def main():
    # Parse arguments
    data = DataProvider()

    # Initialize spreadsheet service
    spreadsheet = SpreadsheetActions(data.token, data.spreadsheet_id, data.new_sheet_index, data.header_formatting,
                                     data.columns)

    # Parse failed tests
    report = ReportParser(data.test_cases_path, data.columns, data.statuses)

    # Set rows and sheet name
    spreadsheet.set_rows(report.rows)
    spreadsheet.set_sheet_name(data.sheet_name)

    # Create new sheet and upload rows
    spreadsheet.create_sheet()
    spreadsheet.upload_rows()

    # Collect requests
    spreadsheet.collect_move_sheet_to_index_request()
    spreadsheet.collect_update_column_size_requests()
    spreadsheet.collect_sort_request()
    spreadsheet.collect_freeze_rows_request()
    spreadsheet.collect_header_formatting_request()
    spreadsheet.collect_horizontal_alignment_requests()
    spreadsheet.collect_set_dropdown_requests()
    spreadsheet.collect_conditional_formatting_to_all_rows()

    # Execute requests
    spreadsheet.execute_requests()

    # Print successful result message
    print('\nUploaded ' + str(report.found_tests_amount) + ' tests with ' + str(data.statuses) +
          ' status(-es) ' + 'on the "' + data.sheet_name + '" sheet:\n' + spreadsheet.get_link_to_sheet())


if __name__ == '__main__':
    main()
