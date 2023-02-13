from __future__ import print_function

from data_provider import DataProvider
from report import ReportParser
from spreadsheet import SpreadsheetActions


def main():
    # Parse arguments
    data = DataProvider()

    # Initialize spreadsheet service
    spreadsheet = SpreadsheetActions(data.token)

    # Parse failed tests
    report = ReportParser(data.test_cases_path, data.columns, data.statuses)
    rows = report.get_rows()

    # Create new sheet and upload rows
    sheet_id = spreadsheet.create_sheet(data.spreadsheet_id, data.sheet_name, data.columns, rows)
    spreadsheet.upload_rows(data.spreadsheet_id, data.sheet_name, rows)

    # Collect requests
    spreadsheet.collect_move_sheet_to_index_request(sheet_id, data.sheet_name, data.new_sheet_index)
    spreadsheet.collect_update_column_size_requests(sheet_id, data.columns)
    spreadsheet.collect_sort_request(sheet_id, data.columns, rows)
    spreadsheet.collect_freeze_rows_request(sheet_id)
    spreadsheet.collect_header_formatting_request(sheet_id, data.header_formatting)
    spreadsheet.collect_horizontal_alignment_requests(sheet_id, data.columns, rows)
    spreadsheet.collect_set_dropdown_requests(sheet_id, data.columns, rows)
    spreadsheet.collect_conditional_formatting_to_all_rows(sheet_id, data.columns, rows)

    # Execute requests
    spreadsheet.execute_requests(data.spreadsheet_id)

    # Print successful result message
    link = spreadsheet.get_link_to_sheet(data.spreadsheet_id, sheet_id)
    print('\nUploaded ' + str(report.found_tests_amount) + ' tests with ' + str(data.statuses) + ' status(-es) ' +
          'on the "' + data.sheet_name + '" sheet:\n' + link)


if __name__ == '__main__':
    main()
