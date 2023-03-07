DEFAULT_CONFIG = {
    # "id": "<your-spreadsheet-id>",
    # "token": "<your-refresh-token>",
    "headerFormatting": {
        "backgroundColor": "blue",
        "horizontalAlignment": "CENTER",
        "textFormat": {
            "foregroundColor": "white",
            "fontSize": 11,
            "bold": True
        }
    },
    "sheetIndex": 0,
    "statuses": ["failed", "broken"],
    "columns": [
        {
            "name": "TEST",
            "size": 700,
            "reportValue": "fullName",
            "formatting": {
                "wrapStrategy": "CLIP",
                "verticalAlignment": "MIDDLE"
            }
        },
        {
            "name": "MESSAGE",
            "size": 250,
            "reportValue": "shortMessage",
            "formatting": {
                "wrapStrategy": "CLIP",
                "verticalAlignment": "MIDDLE"
            }
        },
        {
            "name": "STATUS",
            "size": 100,
            "reportValue": "status",
            "horizontalAlignment": "CENTER",
            "formatting": {
                "wrapStrategy": "CLIP",
                "verticalAlignment": "MIDDLE"
            },
            "conditionalFormatting": [
                {
                    "color": "light_red",
                    "ifValue": "failed"
                },
                {
                    "color": "light_green",
                    "ifValue": "passed"
                },
                {
                    "color": "grey",
                    "ifValue": "skipped"
                },
                {
                    "color": "light_yellow",
                    "ifValue": "broken"
                },
                {
                    "color": "light_purple",
                    "ifValue": "unknown"
                }
            ]
        },
        {
            "name": "REVISION",
            "size": 100,
            "horizontalAlignment": "CENTER",
            "dropdown": ["fixed", "passed", "bug"],
            "formatting": {
                "wrapStrategy": "CLIP",
                "verticalAlignment": "MIDDLE"
            },
            "conditionalFormatting": [
                {
                    "color": "light_green",
                    "ifValue": "fixed"
                },
                {
                    "color": "light_green",
                    "ifValue": "passed"
                },
                {
                    "color": "red",
                    "ifValue": "bug"
                }
            ]
        },
        {
            "name": "COMMENTS",
            "size": 450,
            "formatting": {
                "wrapStrategy": "CLIP",
                "verticalAlignment": "MIDDLE"
            }
        }
    ]
}
