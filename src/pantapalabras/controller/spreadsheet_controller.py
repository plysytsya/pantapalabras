import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pantapalabras.config import settings
from pantapalabras.constants import PROJECT_DIR

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_credentials = ServiceAccountCredentials.from_json_keyfile_name(
    f"{PROJECT_DIR}/client_secret.json", scopes
)


class SpreadsheetController:
    def __init__(self):
        self.client = gspread.authorize(service_account_credentials)
        self.main_sheet = self.client.open(settings.SPREADSHEET).sheet1

    def add_vocabulary_pair(self, lang_a: str, lang_b: str) -> None:
        last_row_index = self.get_last_row_index()
        next_empty_row = last_row_index + 1
        self.main_sheet.update(f"A{next_empty_row}:B{next_empty_row}", [[lang_a, lang_b]])

    def get_last_row_index(
        self,
    ) -> int:
        return len(self.main_sheet.col_values(1))

    def get_whole_spreadsheet(
        self,
    ):
        return self.main_sheet.get_all_records()
