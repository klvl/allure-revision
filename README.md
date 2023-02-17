# Allure Revision

[![Tests](https://github.com/klvl/allure-revision/actions/workflows/pytests.yml/badge.svg)](https://github.com/klvl/allure-revision/actions/workflows/pytests.yml)

The tool to parse allure-report and upload raw results to spreadsheet API.

## Setup

* Clone the project
```shell
git clone https://github.com/klvl/allure-revision
```
* Setup requirements
```shell
pip install -r allure-revision/requirements.txt
```
* Run a script
```shell
python3 main/make.py
```
* Login your Google account
* Click on `Advanced` link, when a "Google hasn't verified this app" page is displayed
* Click on `Go to allure-revision-app (unsafe)` link
* Click `Continue`

Congratulations! The refresh token is copied to your clipboard. Follow [Usage](#usage) section for further usage.


## Usage

Please, complete steps from the [Setup](#setup) section prior to use a tool to obtain a refresh token.

* Create a new Google spreadsheet or open existing  
* Open your spreadsheet, for example [https://docs.google.com/spreadsheets/d/1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8/](https://docs.google.com/spreadsheets/d/1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8/)  
* Find your spreadsheet ID in URL, which is `1GOOG39g3lESP0rEADS5EeetIDtoE9XtRactAndUseE8` in example  
* Generate allure report  
* Run revision  
```shell
python3 main/make.py --id <spreadsheet-id> --token <refresh-token> --report_path path/to/allure-report
```


## Wiki

* [Arguments](https://github.com/klvl/allure-revision/wiki/Arguments)
* [Configurations](https://github.com/klvl/allure-revision/wiki/Configuration)
* [Colors](https://github.com/klvl/allure-revision/wiki/Colors)

