/***** 設定ここから *****/
const REMO_TOKEN = "";  // ← RemoのAPIトークン
const CAMERA_URL = "";  // ← カメラのURL
const MAIL_TO = "";  // ← 自分のGmailアドレス
const SHEET_DATA = "data";      // 照度・人感ログ用シート名
const SHEET_CAPTURE = "capture"; // 撮影ログ用シート名
/***** 設定ここまで *****/

/**
 * Remo 3 から照度・人感データを取得
 */
function getRemoData() {
  const url = "https://api.nature.global/1/devices";
  const headers = { "Authorization": "Bearer " + REMO_TOKEN };

  const response = UrlFetchApp.fetch(url, { "headers": headers });
  const data = JSON.parse(response.getContentText())[0];

  const illuminance = data.newest_events.il.val;
  const motion = data.newest_events.mo.val;

  return { illuminance, motion };
}

/**
 * 照度・人感データを data シートに記録（5分ごと実行想定）
 */
function logRemoData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_DATA);
  const { illuminance, motion } = getRemoData();
  const now = new Date();

  sheet.appendRow([now, illuminance, motion]);
}

/**
 * カメラから画像を取得して Google Drive に保存し、URL を返す
 */
function saveCameraImageToDrive() {
  const cameraUrl = CAMERA_URL;  

  const username = "";  
  const password = "";  
  const auth = Utilities.base64Encode(username + ":" + password);

  const response = UrlFetchApp.fetch(cameraUrl, {
    headers: {
      "Authorization": "Basic " + auth
    },
    muteHttpExceptions: true
  });

  const blob = response.getBlob();
  const timestamp = Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyyMMdd_HHmmss");
  blob.setName(`capture_${timestamp}.jpg`);

  const file = DriveApp.createFile(blob);
  return file.getUrl();
}

/**
 * 画像URLを自分のGmailに送信
 */
function sendImageByEmail(imageUrl, illuminance, motion) {
  const subject = "【自動撮影】人感センサーが反応しました";
  const body =
    "人感センサーが反応しました。\n\n" +
    "照度: " + illuminance + "\n" +
    "motion: " + motion + "\n\n" +
    "画像はこちらから確認できます:\n" + imageUrl;

  GmailApp.sendEmail(MAIL_TO, subject, body);
}

/**
 * 撮影ログを capture シートに記録
 */
function logCapture(illuminance, motion, imageUrl) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_CAPTURE);
  const now = new Date();
  sheet.appendRow([now, illuminance, motion, imageUrl]);
}

/**
 * 人感センサーを見て、反応があれば撮影 → Drive保存 → メール送信 → ログ記録
 */
function cameraTriggerByMotion() {
  const { illuminance, motion } = getRemoData();

  // motion が 1 のときだけ撮影
  if (motion === 1) {
    const imageUrl = saveCameraImageToDrive();
    sendImageByEmail(imageUrl, illuminance, motion);
    logCapture(illuminance, motion, imageUrl);
  }
}