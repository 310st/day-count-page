import os
import datetime
import subprocess

# 🔧【必要に応じて変更】Git管理されているフォルダの絶対パス
repo_dir = r"C:\Users\250634\day-count-page"

# 🔧【変更不要】出力するHTMLファイルのパス
html_path = os.path.join(repo_dir, "non_accident_days.html")

# 🗓️ 起点の日付（無事故カウント開始日）【必要に応じて変更】
start_date = datetime.date(2025, 6, 19)

# 🚫 休業日リスト（土日＋任意の日）
def is_working_day(date):
    if date.weekday() >= 5:  # 5=土, 6=日
        return False
    # 🔧 追加したい休業日があればここに追記
    holidays = [
        datetime.date(2025, 7, 21),  # 海の日
        datetime.date(2025, 8, 11),  # 山の日
    ]
    return date not in holidays

# 📆 無事故日数の計算
today = datetime.date.today()
working_days = sum(
    1 for day in range((today - start_date).days + 1)
    if is_working_day(start_date + datetime.timedelta(days=day))
)

# 📝 HTMLの内容
html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>無事故継続日数</title></head>
<body>
<h1 style="font-size: 2em; text-align: center; margin-top: 100px;">
🚫 無事故継続 <strong>{working_days}</strong> 日
</h1>
</body>
</html>
"""

# 💾 HTMLファイルに出力
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTMLを出力しました: {html_path}")

# ✅ Gitに反映（add → commit → push）
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