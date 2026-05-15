#テストまだ
#envファイル読み込み用
from dotenv import load_dotenv
import os
import smtplib

#API用
import requests
import time
import xml.etree.ElementTree as ET #APIがXML形式のため
from datetime import datetime
from requests.auth import HTTPDigestAuth #Digest認証

#email用
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#envファイル読み込み
load_dotenv()

#カメラ設定
CAMERA_IP = os.getenv("CAMERA_IP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

#Gmail設定
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")

#人数を検知するプログラム
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
    GAS_URL = os.getenv("GAS_URL")

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
    return path,filename

#メール送信
def send_mail(path,filename):

    #添付する画像
    image_path = path

    #メール作成
    msg = MIMEMultipart()

    msg["Subject"] = "【監視カメラ】人検知通知"
    msg["From"] = FROM_ADDRESS
    msg["To"] = TO_ADDRESS
    #本文
    body = "人を検知しました。画像を確認してください。"

    msg.attach(MIMEText(body, "plain"))

    # 画像添付
    with open(image_path, "rb") as f:

        part = MIMEBase("application", "octet-stream")

        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={filename}"
    )

    msg.attach(part)

    #Gmailへ接続
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(FROM_ADDRESS, APP_PASSWORD)

        print("送信開始")
        #メール送信
        server.send_message(msg)
        print("送信完了")

    print("メール送信成功")

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
        path,filename = snapshot()
        #スプレッドシートに書き込み
        write_spreadsheet()
        #メールを送信
        send_mail(path,filename)


    else:
        print("誰もいません")

    #前回人数を保存
    last_count = count

    #1秒ごとに監視する
    time.sleep(1)

#-----------------------------------------------------------