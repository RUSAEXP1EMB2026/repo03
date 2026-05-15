function doPost(e) {

  // スプレッドシート取得
  const sheet = SpreadsheetApp
    .getActiveSpreadsheet()
    .getSheetByName("Sheet1");

  // JSON受信
  const data = JSON.parse(e.postData.contents);

  // 時刻取得
  const now = data.datetime;

  // シートへ書き込み
  sheet.getRange("A1").setValue(now);

  // レスポンス
  return ContentService
    .createTextOutput("OK");
}