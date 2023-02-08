# Allure Revision

The tool to parse allure-report and upload raw results to spreadsheet API.


## Setup

1. Login your google account
2. Enable new API
   * Go to [Google Cloud Console](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
   * Create a project
   * Enable API
3. Get credentials
   * Go to [Credentials](https://console.cloud.google.com/apis/credentials)
   * Click Create Credentials > OAuth client ID
   * Click Application type > Desktop app
   * In the Name field, type a name for the credential
   * Click Create
   * Click OK
   * Save the downloaded JSON file as `credentials.json`
4. Clone repo
   ```shell
   git clone https://github.com/klvl/allure-revision
   ```
5. Move your `credentials.json` file to a `main` folder
   ```shell
   mv ~/Downloads/credentials.json ~/allure-revision/main/ 
   ```


## Usage

```shell
python3 main/make.py --report=/path/to/allure-reprot --sheet=build-7
```