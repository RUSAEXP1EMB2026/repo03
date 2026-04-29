import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SPREADSHEET_NAME = "nature remo"

def save_to_spreadsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scopes
    )

    gc = gspread.authorize(creds)

    sheet = gc.open(SPREADSHEET_NAME).sheet1

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test-device",
        123
    ])

    print("スプレッドシートに書き込みました")

if __name__ == "__main__":
    save_to_spreadsheet()