import requests

# 自分のNature Remoトークン
TOKEN = "ここにNature Remoトークン"

# API認証用ヘッダー
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Nature Remoに登録した「照明ON」のsignal id
LIGHT_ON_SIGNAL_ID = "ここに照明ONのsignal id"

# Nature Remoに登録した「照明OFF」のsignal id
LIGHT_OFF_SIGNAL_ID = "ここに照明OFFのsignal id"

# しきい値
# この値より小さいと暗いと判断する
THRESHOLD = 40

# 指定したsignal idの赤外線信号を送る関数
def send_signal(signal_id):
    url = f"https://api.nature.global/1/signals/{signal_id}/send"

    # POSTで信号送信
    r = requests.post(url, headers=HEADERS)

    # エラーがあればここで止まる
    r.raise_for_status()

# 明るさの値を見て照明を制御する関数
def control_light(current_light, threshold=40):
    # 明るさが取得できなかった場合
    if current_light is None:
        print("明るさが取得できませんでした")
        return

    # しきい値より暗いなら照明ON
    if current_light < threshold:
        send_signal(LIGHT_ON_SIGNAL_ID)
        print("暗いので照明ON")

    # しきい値以上なら照明OFF
    else:
        send_signal(LIGHT_OFF_SIGNAL_ID)
        print("明るいので照明OFF")

# テスト実行
if __name__ == "__main__":
    # 例として手動で明るさを入れて試す
    test_light = 30
    control_light(test_light, threshold=THRESHOLD)