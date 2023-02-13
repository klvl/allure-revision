import json
import pyperclip

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from vars import CREDS, COLORS, COLUMN_NAMES

# If modifying these scopes, the refresh_token should be removed
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class SpreadsheetUtil:
    def __init__(self, token):
        self.service = self.get_service(token)

    # Refer to https://developers.google.com/sheets/api/quickstart/python#configure_the_sample
    @staticmethod
    def get_service(token):
        creds = None
        try:
            if token is not None:
                creds = Credentials.from_authorized_user_info(token, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_config(CREDS, SCOPES)
                    creds = flow.run_local_server(port=0)
                    token = json.loads(creds.to_json())['refresh_token']
                    pyperclip.copy(token)
                    print('\n\nSetup is completed!\n\n' +
                          'Your refresh token is already copied to your clipboard:\n' +
                          token)
                    exit()
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
    def get_update_sheet_index_request(sheet_id, index, sheet_name):
        return {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'index': index,
                    'title': sheet_name
                },
                'fields': 'index,title'
            }
        }

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

    @staticmethod
    def get_repeat_cell_request(sheet_id, start_row_index, end_row_index, background_color, foreground_color,
                                font_size):
        return {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': background_color,
                        'horizontalAlignment': 'CENTER',
                        'textFormat': {
                            'foregroundColor': foreground_color,
                            'fontSize': font_size,
                            'bold': json.dumps(True)
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        }

    @staticmethod
    def get_horizontal_alignment_request(sheet_id, start_row_index, end_row_index, start_column_index,
                                         end_column_index):
        return {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': end_column_index
                },
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': 'CENTER',
                    }
                },
                'fields': 'userEnteredFormat(horizontalAlignment)'
            }
        }

    @staticmethod
    def get_set_dropdown_request(sheet_id, start_row_index, end_row_index, start_column_index, end_column_index,
                                 values):
        return {
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': end_column_index
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': values,
                    },
                    'showCustomUi': json.dumps(True),
                    'strict': json.dumps(True)
                }
            }
        }


class SpreadsheetActions:
    def __init__(self, token):
        self.util = SpreadsheetUtil(token)
        self.requests = []

    # This request should be executed first because we get sheet ID from it
    def create_sheet(self, spreadsheet_id, sheet_name, columns, rows):
        rows_count = len(rows)
        columns_count = len(columns)

        return self.util.create_new_sheet(
            sheet_name, spreadsheet_id, rows_count, columns_count)

    def upload_rows(self, spreadsheet_id, sheet_name, rows):
        self.util.upload_rows(sheet_name, 'A:Z', spreadsheet_id=spreadsheet_id, rows=rows)

    def collect_move_sheet_to_index_request(self, sheet_id, sheet_name, new_sheet_index):
        if new_sheet_index is not None:
            request = self.util.get_update_sheet_index_request(sheet_id, new_sheet_index, sheet_name)
            self.requests.append(request)

    def collect_update_column_size_requests(self, sheet_id, columns):
        for index, column in enumerate(columns):
            if column['size']:
                request = self.util.get_update_column_size_rq(sheet_id, index, column['size'])
                self.requests.append(request)

    def collect_sort_request(self, sheet_id, columns, rows):
        request = self.util.get_sort_request(sheet_id=sheet_id,
                                             start_row_index=1,
                                             end_row_index=len(rows) + 1,
                                             start_column_index=0,
                                             end_column_index=len(columns) + 1,
                                             sort_order='ASCENDING',
                                             dimension_index=0)
        self.requests.append(request)

    def collect_freeze_rows_request(self, sheet_id):
        request = self.util.get_freeze_rows_rq(sheet_id, 1)
        self.requests.append(request)

    def collect_set_dropdown_requests(self, sheet_id, columns, rows):
        for index, column in enumerate(columns):
            if column['dropdown']:
                request = self.util.get_set_dropdown_request(
                    sheet_id=sheet_id,
                    start_row_index=1,
                    end_row_index=len(rows),
                    start_column_index=index,
                    end_column_index=index+1,
                    values=column['dropdown'])
                self.requests.append(request)

    def collect_horizontal_alignment_requests(self, sheet_id, columns, rows):
        for index, column in enumerate(columns):
            if column['horizontalAlignment']:
                request = self.util.get_horizontal_alignment_request(
                    sheet_id=sheet_id,
                    start_row_index=1,
                    end_row_index=len(rows),
                    start_column_index=index,
                    end_column_index=index+1)
                self.requests.append(request)

    def collect_header_formatting_request(self, sheet_id, header_formatting):
        if header_formatting:
            request = self.util.get_repeat_cell_request(
                sheet_id=sheet_id,
                start_row_index=0,
                end_row_index=1,
                background_color=header_formatting['backgroundColor'],
                foreground_color=header_formatting['foregroundColor'],
                font_size=header_formatting['fontSize'])
            self.requests.append(request)

    def collect_conditional_formatting_to_all_rows(self, sheet_id, columns, rows):
        for index, column in enumerate(columns):
            if column['conditionalFormatting']:
                for formatting_rule in column['conditionalFormatting']:
                    formula = self.get_conditional_formatting_formula(index, formatting_rule)
                    color = formatting_rule['color']
                    for column_index in range(len(columns)):
                        request = self.util.get_conditional_formatting_rq(
                            sheet_id=sheet_id,
                            start_column_index=column_index,
                            end_column_index=column_index+1,
                            start_row_index=1,
                            end_row_index=len(rows)+1,
                            formula=formula,
                            color=color)
                        self.requests.append(request)

    @staticmethod
    def get_conditional_formatting_formula(index, formatting_rule):
        cell_ref = COLUMN_NAMES[index] + '2'
        return '=EQ(' + cell_ref + '; "' + formatting_rule['ifValue'] + '")'

    def execute_requests(self, spreadsheet_id):
        self.util.batch_update(spreadsheet_id, self.requests)
        self.requests = []

    @staticmethod
    def get_link_to_sheet(spreadsheet_id, sheet_id):
        return 'https://docs.google.com/spreadsheets/d/' + str(spreadsheet_id) + '/edit#gid=' + str(sheet_id)

