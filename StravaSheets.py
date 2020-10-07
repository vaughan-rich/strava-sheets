import requests
import urllib3
import base64
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------- DEFINE FUNCTIONS ---------- #

def selenium_auth():
	
	# Build Headerless Chrome Webdriver
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=1920x1080")
	browser = webdriver.Chrome(chrome_options=chrome_options)
	
	# Normal Chrome Webdriver
	#browser = webdriver.Chrome()

	print("RUNNING SELENIUM...")

	# Login via FB
	browser.get("https://www.strava.com/oauth/authorize?client_id={{CLIENT_ID}}&scope=activity:read_all&response_type=code&redirect_uri={{REDIRECT_URI}}&approval_prompt=force")
	fb = browser.find_element_by_class_name("fb-button")
	fb.click()

	# Sign-In
	em = browser.find_element_by_id("email")
	pa = browser.find_element_by_id("pass")
	login = browser.find_element_by_id("loginbutton")
	em.send_keys(base64.b64decode("{{BASE64_ENCODED_EMAIL}}").decode("utf-8"))
	pa.send_keys(base64.b64decode("{{BASE64_ENCODED_PASSWORD}}").decode("utf-8"))
	login.click()

	# Authorize w/ Strava
	auth = browser.find_element_by_id("authorize")
	auth.click()

	# Get Current URL
	currentURL = browser.current_url
	browser.quit()

	print("SELENIUM TEST COMPLETE")

	# Capture Parameters
	qps = dict(parse.parse_qsl(parse.urlsplit(currentURL).query))
	print(qps)
	return qps

def request_token():
	print("Requesting Access Token...\n")
	auth_url = "https://www.strava.com/oauth/token"
	qparams = selenium_auth()
	payload = {
	    'client_id': "{{CLIENT_ID}}",
	    'client_secret': '{{CLIENT_SECRET}}',
	    'refresh_token': '{{REFRESH_TOKEN}}',
	    'code':qparams['code'],
	    'grant_type': "authorization_code",
	    'f': 'json'
	}
	res = requests.post(auth_url, data=payload, verify=False)
	access_token = res.json()['access_token']
	print("Access Token = {}\n".format(access_token))
	return access_token

def get_activities():

	access_token = request_token()

	print("Requesting Activities...\n")
	activites_url = "https://www.strava.com/api/v3/athlete/activities"
	header = {'Authorization': 'Bearer ' + access_token}
	param = {'per_page': 200, 'page': 1}
	activities = requests.get(activites_url, headers=header, params=param).json()

	# I removed these fields as I didn't need them
	keysToRemove = ('upload_id_str',
		 'heartrate_opt_out',
		 'workout_type',
		 'comment_count',
		 'trainer',
		 'device_watts',
		 'visibility',
		 'location_city',
		 'has_heartrate',
		 'timezone',
		 'flagged',
		 'gear_id',
		 'from_accepted_tag',
		 'pr_count',
		 'manual',
		 'total_photo_count',
		 'achievement_count',
		 'athlete_count',
		 'location_state',
		 'external_id',
		 'resource_state',
		 'location_country',
		 'utc_offset',
		 'display_hide_heartrate_option',
		 'photo_count',
		 'commute',
		 'private',
		 'has_kudoed',
		 'kudos_count',
		 'start_latlng')
	for activity in activities:
		for k in keysToRemove:
			activity.pop(k, None)
		#print("ACTIVITY: " + activity["name"] + "\n" + json.dumps(activity, indent=1, sort_keys=True) + "\n")

	return activities

# ---------- SHEETS STUFF ---------- #

df = pd.DataFrame(data=get_activities())
print("\n")
#pd.DataFrame(df.end_latlng.tolist(), columns=['end_latitude', 'end_longitude'])
print(df)
print("\n")

gScope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("{{GCP_CREDENTIALS_JSON_FILE}}",gScope)
client = gspread.authorize(creds)
sheet = client.open("{{SPREADSHEET_NAME}}").sheet1
set_with_dataframe(sheet, df)













