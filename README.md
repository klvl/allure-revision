# Allure Revision

The tool to parse allure-report and upload raw results to spreadsheet API.


**Outline:**
* [Setup](#setup)
* [Arguments](#arguments)
* [Configuration](#configuration)


## Setup

* Clone the project
```shell
git clone https://github.com/klvl/allure-revision
```
* Setup requirements
```shell
pip install -r allure-revision/requirements.txt
```
* Create a new Google spreadsheet
* Extract spreadsheet ID from URL(see the [Arguments](#arguments) section to know how to get it)
* Generate allure report
* Run a script 
```shell
python3 main/make.py --report /path/to/allure-reprot --id <your_spreadsheet_id>
```
* Login your Google account, when a web browser is open 
* Click on `Advanced` link, when a 'Google hasn't verified this app' is displayed
* Click on `Go to allure-revision-app (unsafe)` link  
* Click `Continue`  
* Find a `refresh_token` in the output of a script and save it to run app without Google authentication next time   


## Arguments

**--report | Path to allure-report folder**

If this argument is not specified, a script will search for it in current working
directory.

```shell
python3 main/make.py --report path/to/allure-report
```

### --id | Spreadsheet ID

It can be extracted from a spreadsheet URL. For example a spreadsheet ID in the following URL
[https://docs.google.com/spreadsheets/d/1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8/](https://docs.google.com/spreadsheets/d/1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8/)
is `1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8`. If `--id` argument is not specified, the script will look for the
`id` parameter in config.json file, in current working directory.

```shell
python3 main/make.py --id 1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8
```

### --token | Refresh token

You will find you in the script run output, after following steps in the [Setup](#setup) section. It is required to run
script without Google Authorization on web. If `--token` argument is not specified, the script will look for`--token`
parameter in config.json file, in current working directory.

```shell
python3 main/make.py --token 1//079xMTmTOxNswPgXIANACGTcSNwF-O9Br9IEYQw7mKPzZJ9GT2i5e1qWvPGSTfqIdr44Is92yXZw8gEX-d2_JhIRGxNXNwBOonIw
```

### --sheet | Sheet name

When you run a script, it creates new sheet in your spreadsheet. This argument sets a new sheet name. If `--sheet` 
argument is not specified, the name of new sheet will be named as current day and time in a format `MM/DD/YY | HH:MM:SS`.

```shell
python3 main/make.py --sheet build-7
```

### --config | Path to config

See [Config](#configuration) section to know more about a config. If the `--config` argument is not specified, the script will
search for it in current working directory. If the config.json is not found in current working directory, the script 
will use a [default config](#default-config).

```shell
python3 main/make.py --config path/to/config.json
```


## Configuration

There are different configuration options for allure-revision. It is possible to configure statuses of test cases in 
allure-report, columns in a spreadsheet, conditional formatting, dropdown menus and other. The config.json file is used
to configure it and this section describes how to do it.


### How to specify

There are different options to specify config:
* Run a script in directory where a config.json file exists
* Create a config.json file somewhere and run a script with [--config](#--config--path-to-config) argument, passing 
path to a file
* If a file is not present in working directory and [--config](#--config--path-to-config) argument is not specified, a 
[default config](#default-config) will be used


### id [optional]

```json
{
  "id": "1GOOo39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8"
}
```

The `id` parameter is a spreadsheet ID. Read where to find a spreadsheet ID in 
[--id | Spreadsheet ID](#--id--spreadsheet-id) section. If `id` is specified in a config.json and is passed as a CLI
argument, the value from argument will be used.


### token [optional]

```json
{
  "token": "1//079xMTmTOxNswPgXIANACGTcSNwF-O9Br9IEYQw7mKPzZJ9GT2i5e1qWvPGSTfqIdr44Is92yXZw8gEX-d2_JhIRGxNXNwBOonIw"
}
```

The `token` parameter is a refresh token. Read where to find a spreadsheet ID in
[--token | Refresh token](#--token--refresh-token) section. If `token` is specified in a config.json and is passed as a 
CLI argument, the value from argument will be used.


### statuses [mandatory]

```json
{
  "statuses": ["failed", "broken"]
}
```

The `statuses` array specifies which tests statuses it will get from allure report and upload to a spreadsheet. For 
example, if only "failed" status is specified, it will get only tests with "failed" status from allure report and upload
to a spreadsheet. The `statuses` array cannot be empty.

Supported values: "failed", "passed", "skipped", "broken", "unknown"


### newSheetIndex [optional]

```json
{
  "newSheetIndex": 0
}
```

The `newSheetIndex` specifies where to put sheet in a document. If this value is not specified, the new sheet is created
in the end of all sheets in a document.


### headerFormatting [optional]

```json
{
  "headerFormatting": {
    "backgroundColor": "blue",
    "foregroundColor": "white",
    "fontSize": 11
  }
}
```

The `headerFormatting` specifies the first row (header) formatting. The `headerFormatting.backgroundColor` specifies
a background color for header row. The `headerFormatting.foregroundColor` specifies the font color for header row. The
`headerFormatting.fontSize` specifies the font size for a header row. See available `backgroundColor` and 
`foregroundColor` values in a [Colors](#colors) section. 


### columns [mandatory]

```json
{
  "columns": [
    {
      "name": "REVISION",
      "size": 100,
      "index": 3,
      "horizontalAlignment": "CENTER",
      "dropdown": ["fixed", "passed", "bug"],
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
    }
  ]
}
```

The `columns` is array of column json objects. It specifies the columns and its properties which will be displayed in 
allure report. Read about column properties in the following sections. 

### columns.column.name [mandatory]

```json
{
  "columns": [
    {
      "name": "TEST"
    }
  ]
}
```

The `columns.column.name` is a column name which will be displayed in a spreadsheet.


### columns.column.size [optional]

```json
{
  "columns": [
    {
      "size": 100
    }
  ]
}
```

The `columns.column.size` specifies a column size in a spreadsheet, in pixels.


### columns.column.index [mandatory]

```json
{
  "columns": [
    {
      "index": 3
    }
  ]
}
```

The `columns.column.index` specifies a column sequence in a spreadsheet. The index start from 0. It is not allowed to
duplicate indexes. It is not allowed to miss a sequence, e.g. 0, 1, 2, 4, 5 (where 3 is missed).


### columns.column.reportValue [optional]

```json
{
  "columns": [
    {
      "reportValue": "fullName"
    }
  ]
}
```

The `columns.column.reportValue` specifies the information which we want to get from allure report and display in a
spreadsheet. If this value is not specified, the column will be a blank or with a
[dropdown](#columnscolumndropdown-optional) value if specified. The column cannot contain both options together
(`columns.column.reportValue` and `columns.column.dropdown`).

Supported values:
* "fullName" — full test name, e.g. com.package.TestClass.myTestMethodName
* "message" — failure message
* "messageShort" — short failure message (will be displayed only the first line, before "\n")
* "category" — defect category
* "status" — test case status


### columns.column.horizontalAlignment [optional]

```json
{
  "columns": [
    {
      "horizontalAlignment": "CENTER"
    }
  ]
}
```

The `columns.column.horizontalAlignment` specifies a horizontal alignment for all rows for a column.

Supported values: "LEFT", "CENTER", "RIGHT", "JUSTIFYLEFT"


### columns.column.dropdown [optional]

```json
{
  "columns": [
    {
      "dropdown": ["fixed", "passed", "bug"]
    }
  ]
}
```

The `columns.column.dropdown` specifies array of dropdown values for all rows for a given column. The values is a free
string input. If this value is not specified, the column will be a blank or with a
[reportValue](#columnscolumnreportvalue-optional) value if specified. The column cannot contain both options together
(`columns.column.reportValue` and `columns.column.dropdown`). 


### columns.column.conditionalFormatting [optional]

```json
{
  "columns": [
    {
      "conditionalFormatting": [
        {
          "color": "red",
          "ifValue": "failed"
        }
      ]
    }
  ]
}
```

The `columns.column.conditionalFormatting` specifies array of conditional formatting rules. The 
`columns.column.conditionalFormatting.ifValue` specifies the text which triggers a conditional formatting. The 
`columns.column.conditionalFormatting.color` specifies a background color if the value from `ifValue` parameter is 
present in cell. According to example above, if in a given column, in any row, a cell value is "failed", then full row will have a red 
background color. 

The conditional formatting rules are unlimited. The `ifValue` is a free string value. See available colors in a 
[Colors](#colors) section.


### Default config

If the path to config is not specified through [--config](#--config--path-to-config) CLI argument, and it is not present
in working directory, where the script is running from —— the default config will be used.

You can find a default config in the `default_config.json` file.


### Colors

See available color values below.

<div>
    <div>
        black:
    </div>
    <img title="Black" src="img/black.png" width="80" height="19">
    <br>
    <div>
        white:
    </div>
    <img title="White" src="img/white.png" width="80" height="19">
    <br>
    <div>
        grey:
    </div>
    <img title="Grey" src="img/grey.png" width="80" height="19">
    <br>
    <div>
        light_grey:
    </div>
    <img title="Light grey" src="img/light_grey.png" width="80" height="18">
    <br>
    <div>
        red:
    </div>
    <img title="Red" src="img/red.png" width="80" height="18">
    <br>
    <div>
        light_red:
    </div>
    <img title="Light red" src="img/light_red.png" width="80" height="18">
    <br>
    <div>
        orange:
    </div>
    <img title="Orange" src="img/orange.png" width="80" height="18">
    <br>
    <div>
        light_orange:
    </div>
    <img title="Light orange" src="img/light_orange.png" width="80" height="18">
    <br>
    <div>
        yellow:
    </div>
    <img title="Yellow" src="img/yellow.png" width="80" height="18">
    <br>
    <div>
        light_yellow:
    </div>
    <img title="Light yellow" src="img/light_yellow.png" width="80" height="18">
    <br>
    <div>
        green:
    </div>
    <img title="Green" src="img/green.png" width="80" height="18">
    <br>
    <div>
        light_green:
    </div>
    <img title="Light green" src="img/light_green.png" width="80" height="18">
    <br>
    <div>
        blue:
    </div>
    <img title="Blue" src="img/blue.png" width="80" height="18">
    <br>
    <div>
        light_blue:
    </div>
    <img title="Light blue" src="img/light_blue.png" width="80" height="18">
    <br>
    <div>
        purple:
    </div>
    <img title="Purple" src="img/purple.png" width="80" height="18">
    <br>
    <div>
        light_purple:
    </div>
    <img title="Light purple" src="img/light_purple.png" width="80" height="18">
</div>