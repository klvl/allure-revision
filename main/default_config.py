DEFAULT_CONFIG = {
    # 'id': '<your-spreadsheet-id>',
    # 'token': '<your-refresh-token>',
    'headerFormatting': {
        'backgroundColor': 'blue',
        'foregroundColor': 'white',
        'fontSize': 11
    },
    'newSheetIndex': 0,
    'statuses': ['failed', 'broken'],
    'columns': [
        {
            'name': 'TEST',
            'size': 700,
            'reportValue': 'fullName',
            'index': 0
        },
        {
            'name': 'MESSAGE',
            'size': 250,
            'reportValue': 'shortMessage',
            'index': 1
        },
        {
            'name': 'STATUS',
            'size': 100,
            'reportValue': 'status',
            'index': 2,
            'horizontalAlignment': 'CENTER',
            'conditionalFormatting': [
                {
                    'color': 'light_red',
                    'ifValue': 'failed'
                },
                {
                    'color': 'light_green',
                    'ifValue': 'passed'
                },
                {
                    'color': 'grey',
                    'ifValue': 'skipped'
                },
                {
                    'color': 'light_yellow',
                    'ifValue': 'broken'
                },
                {
                    'color': 'light_purple',
                    'ifValue': 'unknown'
                }
            ]
        },
        {
            'name': 'REVISION',
            'size': 100,
            'index': 3,
            'horizontalAlignment': 'CENTER',
            'dropdown': ['fixed', 'passed', 'bug'],
            'conditionalFormatting': [
                {
                    'color': 'light_green',
                    'ifValue': 'fixed'
                },
                {
                    'color': 'light_green',
                    'ifValue': 'passed'
                },
                {
                    'color': 'red',
                    'ifValue': 'bug'
                }
            ]
        },
        {
            'name': 'COMMENTS',
            'size': 500,
            'index': 4
        }
    ]
}