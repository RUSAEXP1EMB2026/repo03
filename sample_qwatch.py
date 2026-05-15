#テストまだ
import requests
import time
import xml.etree.ElementTree as ET #APIがXML形式のため
from datetime import datetime
from requests.auth import HTTPDigestAuth #Digest認証

CAMERA_IP = "192.168.1.214"
USERNAME = "admin"
PASSWORD = "h810"

#写真保存お試しプログラム
def snapshot():

    #検索窓にurl入れてuser名とpassword入れるとその瞬間のsnapshot見れる
    url = f"http://{CAMERA_IP}/snapshot.jpg"

    #APIにリクエスト
    res = requests.get(
        url, auth=HTTPDigestAuth(USERNAME, PASSWORD),
        timeout = 5
    )

    if res.status_code == 200:
        print(res.status_code)
    else:
        print("snapshot取得失敗")
        return -1

    #保存する写真のファイル名作成
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    path = f"/mnt/c/Users/M.Kairiki132932/Desktop/picture/{filename}"

    with open(path, "wb") as f:
        f.write(res.content)

    print("保存できた", filename)

#人数を検知するAPIをたたく
def get_person_count():

    #人数カウントAPI
    url = (
        f"http://{CAMERA_IP}"
        "/camera-cgi/admin/param.cgi"
        "?action=list&group=AIDetection_PC_TotalNumber"
    )

    try:
        
        #APIへアクセス
        res = requests.get(
            url,
            auth = HTTPDigestAuth(USERNAME, PASSWORD),
            timeout = 5
        )

        #XML解析
        root = ET.fromstring(res.text)

        #<TotalNumber>を取得
        total_number = root.find(".//TotalNumber")

        if total_number is None:
            return 0

        #total_number.textで数字を整数として取得している
        return int(total_number.text)

    except Exception as e:

        print("エラー:", e)
        return -1

#AppScriptに書き込むプログラム
def write_spreadsheet():
    #AppsScript URL
    GAS_URL = "https://script.google.com/macros/s/AKfycbzXHfVo2Dm-Tx8GvM2b5wHg4-IiEW84I4utTK4kx9fjLLsdmRjZEJpjygIqzNrG7gjK/exec"

    #現在時刻取得
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    #送信データ
    data = {
        "datetime": now
    }

    #POST送信
    res = requests.post(
        GAS_URL,
        json=data
    )

    print(res.text)

#-----------------------------------------------------------
#main

last_count = 0

print("開始")

while True:

    #現在人数取得
    count = get_person_count()

    print("現在人数:", count)

    # 人を検知した場合
    if last_count == 0 and count > 0:

        print("人を検知しました")

        #写真を撮影
        snapshot()
        
        #スプレッドシートに書き込み
        write_spreadsheet()


    else:
        print("誰もいません")

    #前回人数を保存
    last_count = count

    #1秒ごとに監視する
    time.sleep(1)

#-----------------------------------------------------------