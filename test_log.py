import gspread

from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = "nature remo"

last_capture_time = None

def get_spreadsheet():

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scopes
    )

    gc = gspread.authorize(creds)

    return gc.open(SPREADSHEET_NAME)

# =========================
# captureシート取得
# =========================
def get_capture_sheet():

    spreadsheet = get_spreadsheet()

    return spreadsheet.worksheet("capture")


# =========================
# 最新captureログ取得
# =========================
def get_latest_capture_log():

    sheet = get_capture_sheet()

    rows = sheet.get_all_values()

    # データなし
    if len(rows) <= 1:

        return None

    # 最終行
    return rows[-1]


# =========================
# 新しいcaptureログ確認
# =========================
def check_new_capture():

    global last_capture_time

    latest = get_latest_capture_log()

    if latest is None:

        return False

    # 0列目 = time
    capture_time = latest[0]

    # 新しいログなら
    if capture_time != last_capture_time:

        last_capture_time = capture_time

        print("新しいcaptureログ検知")

        return True

    return False



sheet = get_capture_sheet()

print(sheet.title)