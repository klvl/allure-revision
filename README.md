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
   * In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
   * Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
   * Click OK. The newly created credential appears under OAuth 2.0 Client IDs. 
   * Save the downloaded JSON file as credentials.json, and move the file to your working directory.