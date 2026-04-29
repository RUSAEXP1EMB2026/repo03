import csv
import os
from datetime import datetime

# 保存するCSVファイル名
CSV_FILE = "light_log.csv"

# 明るさをCSVに保存する関数
def save_csv(light_value, filename=CSV_FILE):
    # すでにファイルがあるか確認
    exists = os.path.exists(filename)

    # 追記モードでファイルを開く
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # 初回だけ見出しを書く
        if not exists:
            writer.writerow(["time", "light"])

        # 現在時刻と明るさを1行追加
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            light_value
        ])

# テスト実行
if __name__ == "__main__":
    save_csv(55)
    print("CSVに保存しました")