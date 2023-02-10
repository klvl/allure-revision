CREDS = {
    "installed": {
        "client_id": "555723526226-n96l2mat5jo50bo26hef7g7lt2hrtsd7.apps.googleusercontent.com",
        "project_id": "allure-revisioin",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://localhost"
        ]
    }
}
TOKEN = {
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "555723526226-n96l2mat5jo50bo26hef7g7lt2hrtsd7.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/spreadsheets"]
}
AVAILABLE_REPORT_VALUES = ['fullName', 'message', 'category', 'status']
COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O']
COLORS = {  # rgb scheme, where r = r/255, g = g/255, b = b/255
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
    },
    'blue': {
        'red': 0.235294117647059,
        'green': 0.470588235294118,
        'blue': 0.847058823529412
    },
    'white': {
        'red': 1,
        'green': 1,
        'blue': 1
    }
}
DEFAULT_CONFIG = {
    "newSheetIndex": 0,
    "statuses": ["failed", "broken"],
    "headerFormatting": {
        "backgroundColor": "blue",
        "foregroundColor": "white",
        "fontSize": 11
    },
    "columns": [
        {
            "name": "TEST",
            "size": 700,
            "reportValue": "fullName",
            "index": 0
        },
        {
            "name": "MESSAGE",
            "size": 250,
            "reportValue": "message",
            "index": 1
        },
        {
            "name": "STATUS",
            "size": 100,
            "reportValue": "status",
            "index": 2,
            "conditionalFormatting": [
                {
                    "color": "light_red",
                    "ifValue": "failed"
                },
                {
                    "color": "yellow",
                    "ifValue": "broken"
                }
            ]
        },
        {
            "name": "REVISION",
            "size": 100,
            "index": 3,
            "conditionalFormatting": [
                {
                    "color": "green",
                    "ifValue": "fixed"
                },
                {
                    "color": "green",
                    "ifValue": "passed"
                },
                {
                    "color": "dark_red",
                    "ifValue": "bug"
                }
            ]
        },
        {
            "name": "COMMENTS",
            "size": 500,
            "index": 4
        }
    ]
}

