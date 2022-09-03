import gspread

from pantapalabras.config import settings
from pantapalabras.controller.spreadsheet_controller import SpreadsheetController, service_account_credentials


def test_add_vocabulary_pair():
    # Act
    SpreadsheetController().add_vocabulary_pair("hello", "world")

    # Assert
    client = gspread.authorize(service_account_credentials)
    sheet = client.open(settings.SPREADSHEET).sheet1
    all_records = sheet.get_all_records()

    assert all_records[-1] == {"lang_a": "hello", "lang_b": "world"}

    # Tear Down
    sheet.delete_row(len(all_records) + 1)


def test_get_last_row_index():
    last_row_index = SpreadsheetController().get_last_row_index()

    assert isinstance(last_row_index, int)


def test_get_whole_spreadsheet():
    spreadsheet = SpreadsheetController().get_whole_spreadsheet()

    assert isinstance(spreadsheet, list)
    assert list(spreadsheet[0].keys()) == ["lang_a", "lang_b"]
