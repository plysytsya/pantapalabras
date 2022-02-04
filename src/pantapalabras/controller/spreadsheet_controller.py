import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pantapalabras.constants import PROJECT_DIR

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_credentials = ServiceAccountCredentials.from_json_keyfile_name(
    f"{PROJECT_DIR}/client_secret.json", scopes
)
SPREADSHEET_CLIENT = gspread.authorize(service_account_credentials)
