import os
import datetime
import subprocess

#【必要に応じて変更】Git管理されているフォルダの絶対パス
repo_dir = r"C:\Users\250634\day-count-page"

#【変更不要】出力するHTMLファイルのパス
html_path = os.path.join(repo_dir, "non_accident_days.html")

#起点の日付（無事故カウント開始日）【必要に応じて変更】
start_date = datetime.date(2025, 7, 3)

#休業日リスト（土日＋任意の日）
def is_working_day(date):
    if date.weekday() >= 5:  # 5=土, 6=日
        return False
    #追加したい休業日があればここに追記
    holidays = [
        datetime.date(2025, 7, 21),  # 海の日
        datetime.date(2025, 8, 11),  # 山の日
        datetime.date(2025, 8, 12),  #一斉特別休暇
        datetime.date(2025, 9, 15),  #敬老の日
        datetime.date(2025, 10, 13), #スポーツの日
        datetime.date(2025, 11, 3),  #文化の日 
        datetime.date(2025, 11, 4),  
        datetime.date(2025, 11, 24),
        datetime.date(2025, 12, 29),
        datetime.date(2025, 12, 30),
        datetime.date(2025, 12, 31)
    ]
    return date not in holidays

#無事故日数の計算
today = datetime.date.today()
working_days = sum(
    1 for day in range((today - start_date).days + 1)
    if is_working_day(start_date + datetime.timedelta(days=day))
)

# HTMLの内容
html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>無災害記録表</title>
    <style>
        body {{
            font-family: "Arial", sans-serif;
            background-color: #f7f7f7;
            text-align: center;
            padding: 20px;
            color: #222;
        }}
        .title {{
            font-size: 6em;
            font-weight: bold;
            margin-bottom: 5px;
            border-bottom: 2px solid #222; 
            padding-bottom: 10px;
        }}
        .subtitle {{
            font-size: 4em;
            margin-bottom: 15px;
            color.#555;
        }}
        .plus {{
            color: green;
            font-weight: bold;
        }}
        .counter {{
            font-size: 8em;
            background: #fff;
            border: 5px solid green;
            display: inline-block;
            padding: 30px 60px;
            border-radius: 15px;
            box-shadow: 4px 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 5px;
            transition: transform 0.3s;
        }}
         .counter:hover {{
            transform: scale(1.05);
        }}
        .date-box {{
            font-size: 3em;
            margin-top: 15px;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="title">安全 <span class="plus">＋</span> 第一</div>
    <div class="subtitle">無災害記録表(TCIR)</div>
    <div class="counter"><span style="font-size:150px;">{working_days:,}</span> 日</div>'
    <div class="date-box">
        <div style="font-size: 1.2em;">{start_date.year}年{start_date.month}月{start_date.day}日起算</div>
        <div style="font-size: 1.2em;">{today.year}年{today.month}月{today.day}日現在</div>
    </div>
</body>
</html>

"""

# HTMLファイルに出力
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTMLを出力しました: {html_path}")

# Gitに反映（add → commit → push）
try:
    subprocess.run(["git", "-C", repo_dir, "add", "."], check=True)
    subprocess.run(
        ["git", "-C", repo_dir, "commit", "-m", f"自動更新: {today.isoformat()}"],
        check=True
    )
    subprocess.run(["git", "-C", repo_dir, "push"], check=True)
    print("GitHubに反映しました。")
except subprocess.CalledProcessError as e:
    print("Git操作中にエラーが発生しました:", e)