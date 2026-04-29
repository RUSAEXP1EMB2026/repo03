#<<<<<<< HEAD
import requests

# 自分のNature Remoトークンを入れる
TOKEN = "ここにNature Remoトークン"

# APIにアクセスするときの認証情報
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Nature Remoのデバイス一覧を取得する関数
def get_devices():
    url = "https://api.nature.global/1/devices"

    # APIにGETリクエストを送る
    r = requests.get(url, headers=HEADERS)

    # エラーがあればここで止まる
    r.raise_for_status()

    # JSONをPythonのデータに変換して返す
    return r.json()

# デバイス一覧の中から明るさを探す関数
def get_light_value():
    devices = get_devices()

    # 各デバイスを順番に確認
    for d in devices:
        # newest_events に最新センサーデータが入っている
        newest = d.get("newest_events", {})

        # "il" = illuminance（明るさ）
        if "il" in newest:
            # 明るさの値とデバイス名を返す
            return newest["il"]["val"], d["name"]

    # 明るさセンサーが見つからなかったとき
    return None, None

# このファイルを直接実行したときだけ動く部分
if __name__ == "__main__":
    light, name = get_light_value()

    print("device:", name)
#=======
import requests

# 自分のNature Remoトークンを入れる
TOKEN = "ここにNature Remoトークン"

# APIにアクセスするときの認証情報
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Nature Remoのデバイス一覧を取得する関数
def get_devices():
    url = "https://api.nature.global/1/devices"

    # APIにGETリクエストを送る
    r = requests.get(url, headers=HEADERS)

    # エラーがあればここで止まる
    r.raise_for_status()

    # JSONをPythonのデータに変換して返す
    return r.json()

# デバイス一覧の中から明るさを探す関数
def get_light_value():
    devices = get_devices()

    # 各デバイスを順番に確認
    for d in devices:
        # newest_events に最新センサーデータが入っている
        newest = d.get("newest_events", {})

        # "il" = illuminance（明るさ）
        if "il" in newest:
            # 明るさの値とデバイス名を返す
            return newest["il"]["val"], d["name"]

    # 明るさセンサーが見つからなかったとき
    return None, None

# このファイルを直接実行したときだけ動く部分
if __name__ == "__main__":
    light, name = get_light_value()

    print("device:", name)
#>>>>>>> 99247fa1115fe0d82e677b5ca49061712cb1cc95
    print("light:", light)