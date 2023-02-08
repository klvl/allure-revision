import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetService:
    def __init__(self, spreadsheet_id, sheet_name):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.sheet_id = None
        self.token_file_path = os.path.abspath('main/token.json')
        self.credentials_file_path = os.path.abspath('main/credentials.json')
        # If modifying these scopes, delete the file token.json
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = self.get_service()
        # rgb scheme, where r = r/255, g = g/255, b = b/255
        self.light_red_color = {
            'red': 0.956862745098039,
            'green': 0.8,
            'blue': 0.8
        }
        self.dark_red_color = {
            'red': 0.8,
            'green': 0,
            'blue': 0
        }
        self.light_yellow_color = {
            'red': 1,
            'green': 0.949019607843137,
            'blue': 0.8
        }
        self.light_green_color = {
            'red': 0.850980392156863,
            'green': 0.917647058823529,
            'blue': 0.827450980392157
        }

    # Refer to https://developers.google.com/sheets/api/quickstart/python#configure_the_sample
    def get_service(self):
        print('Get spreadsheet service...')
        creds = None
        try:
            if os.path.exists(self.token_file_path):
                creds = Credentials.from_authorized_user_file(self.token_file_path, self.scopes)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file_path, self.scopes)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self.token_file_path, 'w') as token:
                    token.write(creds.to_json())
            return build('sheets', 'v4', credentials=creds)
        except HttpError as err:
            print(err)

    def batch_update(self, requests):
        body = {'requests': requests}
        response = None
        try:
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body).execute()
        except HttpError as err:
            print(err)

        print(str(response) + '\n')
        return response

    def create_new_sheet(self):
        print('Create new sheet with ' + self.sheet_name + ' sheet name...')
        requests = [{
            'addSheet': {
                'properties': {
                    'title': self.sheet_name,
                }
            }
        }]

        response = self.batch_update(requests)
        self.sheet_id = response.get('replies')[0].get('addSheet').get('properties').get('sheetId')

    def upload_rows(self, rows):
        print('Populate sheet with rows...')
        input_range = self.sheet_name + '!A:G'
        value_range_body = {
            'range': input_range,
            'values': rows
        }

        response = None
        try:
            response = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=input_range,
                valueInputOption='RAW',
                body=value_range_body).execute()
        except HttpError as err:
            print(err)

        print(str(response) + '\n')

    def delete_dimension(self, dimension, start_index, end_index):
        print('Delete from ' + str(start_index) + ' to ' + str(end_index) + ' ' + dimension + ' on ' +
              self.sheet_name + ' sheet...')
        requests = [{
            'deleteDimension': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': dimension,
                    'startIndex': start_index,
                    'endIndex': end_index
                }
            }
        }]

        response = self.batch_update(requests)
        return response

    def delete_extra_columns(self, columns_length):
        self.delete_dimension('COLUMNS', columns_length, 26)

    def delete_extra_rows(self, rows_length):
        self.delete_dimension('ROWS', rows_length, 1000)

    def update_dimension(self, dimension, start_index, end_index, pixel_size):
        print('Update ' + dimension + ' dimension from ' + str(start_index) + ' to ' + str(end_index) + ', for ' +
              str(pixel_size) + ' pixels, on ' + self.sheet_name + ' sheet...')
        requests = [{
            'updateDimensionProperties': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': dimension,
                    'startIndex': start_index,
                    'endIndex': end_index
                },
                'properties': {
                    'pixelSize': pixel_size
                },
                'fields': 'pixelSize'
            }
        }]

        response = self.batch_update(requests)
        return response

    def update_column_size(self, column_index, pixel_size):
        self.update_dimension('COLUMNS', column_index, column_index+1, pixel_size)

    def sort(self, start_row_index, end_row_index, start_column_index, end_column_index, sort_order, dimension_index):
        print('Sort the first column ascending...')
        requests = [{
            'sortRange': {
                'range': {
                    'sheetId': self.sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index+1,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': end_column_index+1
                },
                'sortSpecs': [{
                    'sortOrder': sort_order,
                    'dimensionIndex': dimension_index
                }]
            }
        }]
        self.batch_update(requests)

    def freeze_rows(self, rows_count):
        print('Freeze the first ' + str(rows_count) + ' row(s)...')
        requests = [{
            'updateSheetProperties': {
                'properties': {
                    'sheetId': self.sheet_id,
                    'gridProperties': {
                        'frozenRowCount': rows_count
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }]
        self.batch_update(requests)

    def add_conditional_formatting(self, start_column_index, end_column_index, start_row_index, end_row_index, formula,
                                   color):
        requests = [{
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [
                        {
                            'sheetId': self.sheet_id,
                            'startColumnIndex': start_column_index,
                            'endColumnIndex': end_column_index,
                            'startRowIndex': start_row_index,
                            'endRowIndex': end_row_index
                        }
                    ],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [
                                {
                                    'userEnteredValue': formula
                                }
                            ]
                        },
                        'format': {
                            'backgroundColor': color
                        }
                    }
                },
                'index': 0
            }
        }]
        self.batch_update(requests)

    def add_conditional_formatting_to_all_rows(self, columns_length, rows_length, formula, color):
        print('Add conditional formatting...')
        for column in range(columns_length):
            self.add_conditional_formatting(column, column+1, 1, rows_length+1, formula, color)

    def add_conditional_formatting_to_all_rows_light_red(self, columns_length, rows_length, formula):
        self.add_conditional_formatting_to_all_rows(columns_length, rows_length, formula, self.light_red_color)

    def add_conditional_formatting_to_all_rows_dark_red(self, columns_length, rows_length, formula):
        self.add_conditional_formatting_to_all_rows(columns_length, rows_length, formula, self.dark_red_color)

    def add_conditional_formatting_to_all_rows_yellow(self, columns_length, rows_length, formula):
        self.add_conditional_formatting_to_all_rows(columns_length, rows_length, formula, self.light_yellow_color)

    def add_conditional_formatting_to_all_rows_green(self, columns_length, rows_length, formula):
        self.add_conditional_formatting_to_all_rows(columns_length, rows_length, formula, self.light_green_color)

    def get_link_to_sheet(self):
        return 'https://docs.google.com/spreadsheets/d/' + str(self.spreadsheet_id) + '/edit#gid=' + str(self.sheet_id)
