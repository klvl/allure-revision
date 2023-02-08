from __future__ import print_function

from arguments_parser import ArgumentsParser
from report_parser import ReportParser
from spreadsheet_service import SpreadsheetService

# The ID of a spreadsheet
SPREADSHEET_ID = '1EKAU39h3YQCr0kQZCF5DnxuWPxgJ9IoOaumRkbHtCf8'


def main():
    # Parse arguments
    args = ArgumentsParser()
    path = args.get_report_path()
    build_id = args.get_build_id()

    # Parse failed tests
    report = ReportParser(path)
    rows = report.get_rows()

    # Get rows and columns length
    rows_length = len(rows)
    columns_length = len(report.header)

    # Initialize service, create new sheet, upload rows
    spreadsheet = SpreadsheetService(SPREADSHEET_ID, build_id)
    spreadsheet.create_new_sheet()
    spreadsheet.upload_rows(rows)

    # Delete extra columns and rows
    spreadsheet.delete_extra_columns(columns_length)
    spreadsheet.delete_extra_rows(rows_length)

    # Update column sizes
    spreadsheet.update_column_size(0, 700)
    spreadsheet.update_column_size(1, 250)
    spreadsheet.update_column_size(2, 200)
    spreadsheet.update_column_size(3, 80)
    spreadsheet.update_column_size(4, 80)
    spreadsheet.update_column_size(5, 300)

    # Sort tests
    spreadsheet.sort(1, rows_length, 0, columns_length, 'ASCENDING', 0)

    # Freeze header column
    spreadsheet.freeze_rows(1)

    # Set conditional formatting
    spreadsheet.add_conditional_formatting_to_all_rows_light_red(columns_length, rows_length, '=EQ(D2, "failed")')
    spreadsheet.add_conditional_formatting_to_all_rows_yellow(columns_length, rows_length, '=EQ(D2, "broken")')
    spreadsheet.add_conditional_formatting_to_all_rows_green(columns_length, rows_length, '=EQ(E2, "fixed")')
    spreadsheet.add_conditional_formatting_to_all_rows_green(columns_length, rows_length, '=EQ(E2, "passed")')
    spreadsheet.add_conditional_formatting_to_all_rows_dark_red(columns_length, rows_length, '=EQ(E2, "bug")')

    # Print successful result message
    print('Aggregation was successful! To check results, follow this link:\n' + spreadsheet.get_link_to_sheet())


if __name__ == '__main__':
    main()
