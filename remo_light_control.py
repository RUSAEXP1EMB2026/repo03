<<<<<<< HEAD
import requests
import time
import csv
import os
from datetime import datetime

# =========================
# 設定
# =========================

# Nature Remoトークン
TOKEN = "ここにNature Remoトークン"

# API認証用ヘッダー
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# 照明ON/OFFのsignal id
LIGHT_ON_SIGNAL_ID = "ここに照明ONのsignal id"
LIGHT_OFF_SIGNAL_ID = "ここに照明OFFのsignal id"

# 明るさのしきい値
THRESHOLD = 40

# 保存するCSVファイル名
CSV_FILE = "light_log.csv"


# =========================
# デバイス一覧取得
# =========================
def get_devices():
    url = "https://api.nature.global/1/devices"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


# =========================
# 明るさ取得
# =========================
def get_light_value():
    devices = get_devices()

    for d in devices:
        newest = d.get("newest_events", {})

        # "il" があれば明るさデータあり
        if "il" in newest:
            return newest["il"]["val"], d["name"]

    return None, None


# =========================
# 赤外線信号送信
# =========================
def send_signal(signal_id):
    url = f"https://api.nature.global/1/signals/{signal_id}/send"
    r = requests.post(url, headers=HEADERS)
    r.raise_for_status()


# =========================
# 明るさで照明制御
# =========================
def control_light(current_light, threshold=THRESHOLD):
    if current_light is None:
        print("明るさ取得失敗")
        return

    if current_light < threshold:
        send_signal(LIGHT_ON_SIGNAL_ID)
        print("暗いので照明ON")
    else:
        send_signal(LIGHT_OFF_SIGNAL_ID)
        print("明るいので照明OFF")


# =========================
# CSV保存
# =========================
def save_csv(light_value, filename=CSV_FILE):
    exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["time", "light"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            light_value
        ])


# =========================
# メインループ
# =========================
def main():
    print("プログラム開始")

    while True:
        try:
            # 明るさ取得
            light, name = get_light_value()

            # 現在の情報を表示
            print(f"[{datetime.now()}] device={name}, light={light}")

            # CSV保存
            save_csv(light)

            # 照明制御
            control_light(light)

        except Exception as e:
            print("エラー:", e)

        # 5分待つ
        time.sleep(300)


# =========================
# 実行開始
# =========================
if __name__ == "__main__":
=======
import requests
import time
import csv
import os
from datetime import datetime

# =========================
# 設定
# =========================

# Nature Remoトークン
TOKEN = "ここにNature Remoトークン"

# API認証用ヘッダー
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# 照明ON/OFFのsignal id
LIGHT_ON_SIGNAL_ID = "ここに照明ONのsignal id"
LIGHT_OFF_SIGNAL_ID = "ここに照明OFFのsignal id"

# 明るさのしきい値
THRESHOLD = 40

# 保存するCSVファイル名
CSV_FILE = "light_log.csv"


# =========================
# デバイス一覧取得
# =========================
def get_devices():
    url = "https://api.nature.global/1/devices"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


# =========================
# 明るさ取得
# =========================
def get_light_value():
    devices = get_devices()

    for d in devices:
        newest = d.get("newest_events", {})

        # "il" があれば明るさデータあり
        if "il" in newest:
            return newest["il"]["val"], d["name"]

    return None, None


# =========================
# 赤外線信号送信
# =========================
def send_signal(signal_id):
    url = f"https://api.nature.global/1/signals/{signal_id}/send"
    r = requests.post(url, headers=HEADERS)
    r.raise_for_status()


# =========================
# 明るさで照明制御
# =========================
def control_light(current_light, threshold=THRESHOLD):
    if current_light is None:
        print("明るさ取得失敗")
        return

    if current_light < threshold:
        send_signal(LIGHT_ON_SIGNAL_ID)
        print("暗いので照明ON")
    else:
        send_signal(LIGHT_OFF_SIGNAL_ID)
        print("明るいので照明OFF")


# =========================
# CSV保存
# =========================
def save_csv(light_value, filename=CSV_FILE):
    exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["time", "light"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            light_value
        ])


# =========================
# メインループ
# =========================
def main():
    print("プログラム開始")

    while True:
        try:
            # 明るさ取得
            light, name = get_light_value()

            # 現在の情報を表示
            print(f"[{datetime.now()}] device={name}, light={light}")

            # CSV保存
            save_csv(light)

            # 照明制御
            control_light(light)

        except Exception as e:
            print("エラー:", e)

        # 5分待つ
        time.sleep(300)


# =========================
# 実行開始
# =========================
if __name__ == "__main__":
>>>>>>> 99247fa1115fe0d82e677b5ca49061712cb1cc95
    main()