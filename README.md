# Strava Sheets 🏃‍♂️

Strava Sheets pulls your Strava data into a Google Sheet, to analyse/visualise as you please.

![Forrest](runForrestRun.gif)

## How it works:
* Strava Sheets is a Selenium WebDriver script that visits a Strava OAuth Authorisation page and automatically logs you in via the 'Log in with Facebook' button. In order to log in via a different method, lines 33 to 42 of the script would need to be adapted.
* Once authorised, the script pulls various data from all of your Strava activities, and pushes these into a Google Sheet of your choice.

## Setup:
* Install [Selenium WebDriver for Python](https://selenium-python.readthedocs.io/installation.html), along with all the packages referenced at the top of the script (e.g. Pandas, gspread, etc).
* Create your own Strava API Application. A 'Getting Started Guide' can be found [here](http://developers.strava.com).
* Required amendments to the Python script:
  * Line 22 - choose whether to go 'headless' or not, and comment/uncomment the code accordingly.
  * Line 32 - fill in {{CLIENT_ID}} and {{REDIRECT_URI}} with the values found in your Strava Application settings. 
  * Lines 40 to 41 - fill in {{BASE64_ENCODED_EMAIL}} and {{BASE64_ENCODED_PASSWORD}} with your Facebook username and password, but base64-encoded. Because this information is exposed within the code, **please use caution and adapt the script for personal use only**. The encoding is just a quick and dirty attempt to obfuscate, to combat shoulder-surfers.
  * Line 64 to 66 - fill in {{CLIENT_ID}}, {{CLIENT_SECRET}} and {{REFRESH_TOKEN}} with the values found in your Strava Application settings. 
  * Line 87 - this is a list of fields I wasn't interested in pulling into Sheets, personally. Any here that you want to look at should be removed from the list.
  * Line 133 - replace {{GCP_CREDENTIALS_JSON_FILE}} with the name of your GCP credentials JSON file (this is required to use the Sheets API). You can generate these credentials [in the GCP console](http://cloud.google.com/iam/docs/creating-managing-service-account-keys).
  * Line 135 - replace {{SPREADSHEET_NAME}} with the name of your Google spreadsheet. The sheet needs to be shared with the email address found in the GCP credentials file (the value of the 'client_email' key), so that the script is allowed to edit the sheet.

## Usage:
* Run StravaSheets.py

## In Future Versions:
* Improve security (encryption/obfuscation of login details and Strava credentials).
* Add more convenient/flexibile options for a user to choose their login method.
