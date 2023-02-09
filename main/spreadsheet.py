import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetUtil:
    def __init__(self):
        # If modifying these scopes, delete the file token.json
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.token_file_path = os.path.abspath('main/token.json')
        self.credentials_file_path = os.path.abspath('main/credentials.json')
        self.service = self.get_service()

    # Refer to https://developers.google.com/sheets/api/quickstart/python#configure_the_sample
    def get_service(self):
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

    # This request should be executed first because we get sheet ID from it
    def create_new_sheet(self, sheet_name, spreadsheet_id, row_count, column_count):
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name,
                    'gridProperties': {
                        'rowCount': row_count,
                        'columnCount': column_count
                    }
                },
            }
        }]
        response = self.batch_update(spreadsheet_id, requests)
        return response.get('replies')[0].get('addSheet').get('properties').get('sheetId')

    def batch_update(self, spreadsheet_id, requests):
        body = {'requests': requests}
        response = None
        try:
            response = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        except HttpError as err:
            print(err)

        return response

    def upload_rows(self, sheet_name, input_range, spreadsheet_id, rows):
        input_range = sheet_name + '!' + input_range
        value_range_body = {
            'range': str(input_range),
            'values': rows
        }

        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=input_range,
                valueInputOption='RAW',
                body=value_range_body).execute()
        except HttpError as err:
            print(err)


class SpreadsheetActions:
    def __init__(self, config, sheet_name, rows):
        self.config = config
        self.sheet_name = sheet_name
        self.rows = rows
        self.sheet_id = None
        # rgb scheme, where r = r/255, g = g/255, b = b/255
        self.COLORS = {
            "light_red": {
                'red': 0.956862745098039,
                'green': 0.8,
                'blue': 0.8
            },
            'dark_red': {
                'red': 0.8,
                'green': 0,
                'blue': 0
            },
            'yellow': {
                'red': 1,
                'green': 0.949019607843137,
                'blue': 0.8
            },
            'green': {
                'red': 0.850980392156863,
                'green': 0.917647058823529,
                'blue': 0.827450980392157
            }
        }
        self.requests = []
        self.util = SpreadsheetUtil()

    # This request should be executed first because we get sheet ID from it
    def create_sheet(self):
        rows_count = len(self.rows)
        columns_count = len(self.config.columns)

        self.sheet_id = self.util.create_new_sheet(
            self.sheet_name, self.config.spreadsheet_id, rows_count, columns_count)

    def upload_rows(self):
        self.util.upload_rows(self.sheet_name, 'A:Z', spreadsheet_id=self.config.spreadsheet_id, rows=self.rows)

    def get_update_dimension_rq(self, dimension, start_index, end_index, pixel_size):
        return {
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
        }

    def collect_update_column_size_rq(self, column_index, pixel_size):
        self.requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': column_index,
                    'endIndex': column_index + 1
                },
                'properties': {
                    'pixelSize': pixel_size
                },
                'fields': 'pixelSize'
            }
        })

    def collect_sort_rq(self, start_row_index, start_column_index, sort_order, dimension_index):
        self.requests.append({
            'sortRange': {
                'range': {
                    'sheetId': self.sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': len(self.rows)+1,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': len(self.config.columns)+1
                },
                'sortSpecs': [{
                    'sortOrder': sort_order,
                    'dimensionIndex': dimension_index
                }]
            }
        })

    def collect_freeze_rows_rq(self, freeze_first_rows_amount):
        self.requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': self.sheet_id,
                    'gridProperties': {
                        'frozenRowCount': freeze_first_rows_amount
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        })

    def collect_conditional_formatting_rq(self, start_column_index, end_column_index, start_row_index, end_row_index,
                                          formula, color):
        self.requests.append({
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
        })

    def collect_conditional_formatting_to_all_rows(self, formula, color):
        for column in range(len(self.config.columns)):
            self.collect_conditional_formatting_rq(column, column + 1, 1, len(self.rows) + 1, formula, self.COLORS[color])

    def execute_requests(self):
        self.util.batch_update(self.config.spreadsheet_id, self.requests)
        self.requests = []

    def get_link_to_sheet(self):
        return 'https://docs.google.com/spreadsheets/d/' + str(self.config.spreadsheet_id) + '/edit#gid=' + \
               str(self.sheet_id)
