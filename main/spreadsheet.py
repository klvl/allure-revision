import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetUtil:
    def __init__(self, creds, token):
        # If modifying these scopes, the refresh_token should be removed
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.pre_defined_creds = creds
        self.token = token
        self.service = self.get_service()

    # Refer to https://developers.google.com/sheets/api/quickstart/python#configure_the_sample
    def get_service(self):
        creds = None
        try:
            if self.token is not None:
                creds = Credentials.from_authorized_user_info(self.token, self.scopes)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_config(self.pre_defined_creds, self.scopes)
                    creds = flow.run_local_server(port=0)
                    token = json.loads(creds.to_json())['refresh_token']
                    print('Save your "refresh_token" to run without login next time:\n' + token + "\n")
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
        response = None
        try:
            response = self.batch_update(spreadsheet_id, requests)
        except HttpError as err:
            if err.reason == 'Requested entity was not found.':
                print('The Google API did not find your spreadsheet! Check your spreadsheet_id and try again!')
                exit()
            else:
                print("Something went wrong! Contact developer for assistance!")
                exit()
        return response.get('replies')[0].get('addSheet').get('properties').get('sheetId')

    def batch_update(self, spreadsheet_id, requests):
        body = {'requests': requests}
        return self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

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

    @staticmethod
    def get_update_dimension_rq(sheet_id, dimension, start_index, end_index, pixel_size):
        return {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
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

    @staticmethod
    def get_update_column_size_rq(sheet_id, column_index, pixel_size):
        return {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': column_index,
                    'endIndex': column_index + 1
                },
                'properties': {
                    'pixelSize': pixel_size
                },
                'fields': 'pixelSize'
            }
        }

    @staticmethod
    def get_sort_request(sheet_id, start_row_index, end_row_index, start_column_index, end_column_index,
                         sort_order, dimension_index):
        return {
            'sortRange': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': end_column_index
                },
                'sortSpecs': [{
                    'sortOrder': sort_order,
                    'dimensionIndex': dimension_index
                }]
            }
        }

    @staticmethod
    def get_freeze_rows_rq(sheet_id, freeze_first_rows_amount):
        return {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': freeze_first_rows_amount
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }

    @staticmethod
    def get_conditional_formatting_rq(sheet_id, start_column_index, end_column_index, start_row_index, end_row_index,
                                      formula, color):
        return {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [
                        {
                            'sheetId': sheet_id,
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
        }


class SpreadsheetActions:
    def __init__(self, config, sheet_name, rows):
        self.config = config
        self.sheet_name = sheet_name
        self.rows = rows
        self.sheet_id = None
        self.colors = self.config.colors
        self.requests = []
        self.util = SpreadsheetUtil(self.config.creds, self.config.token)

    # This request should be executed first because we get sheet ID from it
    def create_sheet(self):
        rows_count = len(self.rows)
        columns_count = len(self.config.columns)

        self.sheet_id = self.util.create_new_sheet(
            self.sheet_name, self.config.spreadsheet_id, rows_count, columns_count)

    def upload_rows(self):
        self.util.upload_rows(self.sheet_name, 'A:Z', spreadsheet_id=self.config.spreadsheet_id, rows=self.rows)

    def collect_update_column_size_requests(self):
        for column in self.config.columns:
            if column['size']:
                request = self.util.get_update_column_size_rq(self.sheet_id, column['index'], column['size'])
                self.requests.append(request)

    def collect_sort_request(self):
        request = self.util.get_sort_request(sheet_id=self.sheet_id,
                                             start_row_index=1,
                                             end_row_index=len(self.rows) + 1,
                                             start_column_index=0,
                                             end_column_index=len(self.config.columns) + 1,
                                             sort_order='ASCENDING',
                                             dimension_index=0)
        self.requests.append(request)

    def collect_freeze_rows_request(self):
        request = self.util.get_freeze_rows_rq(self.sheet_id, 1)
        self.requests.append(request)

    def collect_conditional_formatting_to_all_rows(self):
        for column in self.config.columns:
            if column['conditionalFormatting']:
                for formatting_rule in column['conditionalFormatting']:
                    formula = self.get_conditional_formatting_formula(column, formatting_rule)
                    color = self.colors[formatting_rule['color']]
                    for column_index in range(len(self.config.columns)):
                        request = self.util.get_conditional_formatting_rq(
                            sheet_id=self.sheet_id,
                            start_column_index=column_index,
                            end_column_index=column_index+1,
                            start_row_index=1,
                            end_row_index=len(self.rows)+1,
                            formula=formula,
                            color=color)
                        self.requests.append(request)

    def get_conditional_formatting_formula(self, column, formatting_rule):
        cell_ref = self.config.column_names[column['index']] + '2'
        return '=EQ(' + cell_ref + '; "' + formatting_rule['ifValue'] + '")'

    def execute_requests(self):
        self.util.batch_update(self.config.spreadsheet_id, self.requests)
        self.requests = []

    def get_link_to_sheet(self):
        return 'https://docs.google.com/spreadsheets/d/' + str(self.config.spreadsheet_id) + '/edit#gid=' + \
               str(self.sheet_id)

