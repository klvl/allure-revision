CREDS = {
    'installed': {
        'client_id': '555723526226-n96l2mat5jo50bo26hef7g7lt2hrtsd7.apps.googleusercontent.com',
        'project_id': 'allure-revisioin',
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
        'client_secret': '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',
        'redirect_uris': [
            'http://localhost'
        ]
    }
}
TOKEN = {
    'token_uri': 'https://oauth2.googleapis.com/token',
    'client_id': '555723526226-n96l2mat5jo50bo26hef7g7lt2hrtsd7.apps.googleusercontent.com',
    'client_secret': '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',
    'scopes': ['https://www.googleapis.com/auth/spreadsheets']
}
AVAILABLE_REPORT_STATUSES = ['failed', 'passed', 'skipped', 'broken', 'unknown']
AVAILABLE_REPORT_VALUES = ['name', 'fullName', 'package', 'epic', 'shortMessage', 'message', 'stepFailed', 'category',
                           'status', 'durationMs', 'durationSec', 'durationMin', 'durationHrs']
AVAILABLE_HORIZONTAL_ALIGNMENTS = ['LEFT', 'CENTER', 'RIGHT', 'JUSTIFYLEFT']
COLUMN_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O']
COLORS = {  # https://kierandixon.com/google-sheets-colors/
    'black': {  # black
        'red': 0,  # 0/255
        'green': 0,  # 0/255
        'blue': 0  # 0/255
    },
    'white': {  # white
        'red': 1,  # 255/255
        'green': 1,  # 255/255
        'blue': 1  # 255/255
    },
    'grey': {  # grey
        'red': 0.8,  # 204/255
        'green': 0.8,  # 204/255
        'blue': 0.8  # 204/255
    },
    'light_grey': {  # light grey 3
        'red': 0.952941176470588,  # 243/255
        'green': 0.952941176470588,  # 243/255
        'blue': 0.952941176470588  # 243/255
    },
    'red': {  # light red 1
        'red': 0.87843137254902,  # 224/255
        'green': 0.4,  # 102/255
        'blue': 0.4  # 102/255
    },
    'light_red': {  # light red 3
        'red': 0.956862745098039,  # 244/255
        'green': 0.8,  # 204/255
        'blue': 0.8  # 204/255
    },
    'orange': {  # dark orange 1
        'red': 0.901960784313725,  # 230/255
        'green': 0.568627450980392,  # 145/255
        'blue': 0.219607843137255  # 56/255
    },
    'light_orange': {  # light orange 2
        'red': 0.976470588235294,  # 249/255
        'green': 0.796078431372549,  # 203/255
        'blue': 0.611764705882353  # 156/255
    },
    'yellow': {  # light yellow 1
        'red': 1,  # 255/255
        'green': 0.850980392156863,  # 217/255
        'blue': 0.4  # 102/255
    },
    'light_yellow': {  # light yellow 3
        'red': 1,  # 255/255
        'green': 0.949019607843137,  # 242/255
        'blue': 0.8  # 204/255
    },
    'green': {  # light green 1
        'red': 0.576470588235294,  # 147/255
        'green': 0.768627450980392,  # 196/255
        'blue': 0.490196078431373  # 125/255
    },
    'light_green': {  # light green 3
        'red': 0.850980392156863,  # 217/255
        'green': 0.917647058823529,  # 234/255
        'blue': 0.827450980392157  # 211/255
    },
    'blue': {  # dark cornflower blue 1
        'red': 0.235294117647059,  # 60/255
        'green': 0.470588235294118,  # 120/255
        'blue': 0.847058823529412  # 216/255
    },
    'light_blue': {  # light cornflower blue 3
        'red': 0.788235294117647,  # 201/255
        'green': 0.854901960784314,  # 218/255
        'blue': 0.972549019607843  # 248/255
    },
    'purple': {  # dark purple 1
        'red': 0.403921568627451,  # 103/255
        'green': 0.305882352941176,  # 78/255
        'blue': 0.654901960784314  # 167/255
    },
    'light_purple': {  # light purple 2
        'red': 0.705882352941176,  # 180/255
        'green': 0.654901960784314,  # 167/255
        'blue': 0.83921568627451  # 214/255
    }
}

