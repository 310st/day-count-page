import os
import datetime
import subprocess

#【必要に応じて変更】Git管理されているフォルダの絶対パス
repo_dir = r"C:\Users\250634\day-count-page"

#【変更不要】出力するHTMLファイルのパス
html_path = os.path.join(repo_dir, "non_accident_days.html")

#起点の日付（無事故カウント開始日）【必要に応じて変更】
start_date = datetime.date(2025, 8, 16)

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
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>無災害記録表</title>

<style>
/* ------------- カラー設定 ------------- */
:root {{
  --primary   : #00A9E0;   /* TELカラー青 */
  --secondary : #78BE20;   /* TELカラーミドリ*/
  --bg-light  : #00A9E0;   /* 背景、TEL青 */
}}

/* -------- Reset -------- */
* {{ box-sizing:border-box; margin:0; padding:0; }}

/* -------- Layout -------- */
html,body {{ height:100%; }}
body {{
  font-family: "Meiryo", Arial, sans-serif;
  background:var(--bg-light);
  color:#222;
  display:grid;
  grid-template-rows:auto 1fr 60px;  /* header - main - footer */
}}

/* -------- Header -------- */
header {{
  display:flex;
  justify-content:center;
  align-items:center;
  background:transparent;  /* 帯や影を消す */
  padding:25px 0 8px 0;
}}
header .logo {{
  font-size:clamp(56px, 10vw, 140px);  /* 画面幅に応じて伸縮 */
  font-weight:700;                     /* 普通の太字 */
  letter-spacing:4px;
  line-height:1;
  color:#fff;
}}

/* 十字の色指定 */
.cross {{
  color: var(--secondary);           /* 緑色 */
  -webkit-text-stroke: 3.5px white; /* 太い白縁取り */
  /* text-stroke は省略してもOK */
  font-weight: 700;                  /* 太字に */
  font-size: 1.5em;                  /* 大きめにして太く見せる */
  text-shadow: 
    -1px -1px 0 white,
    1px -1px 0 white,
    -1px 1px 0 white,
    1px 1px 0 white;                /* 縁取りフォールバック */
}}

/* -------- Main -------- */
main {{
  display:flex;
  justify-content:center;
  align-items:center;
  padding:4px;
}}

.card {{
  background:#fff;
  border:1px solid #e0e0e0;
  border-radius:12px;
  padding:40px 60px;
  box-shadow:0 10px 35px rgba(0,0,0,0.08);
  min-width:60vw;
  max-width:1000px;
  text-align:center;
}}
.card h2 {{
  font-size:4.1rem;
  color:var(--primary);
  margin-bottom:1px;
  font-weight:700;
}}
.counter {{
  font-size:clamp(100px, 16vw, 240px);
  color:var(--secondary);
  font-weight:700;
  line-height:1;
  margin:10px 0 14px;
}}
.counter small {{
  font-size:0.18em;
  font-weight:500;
  margin-left:10px;
}}
.date-box {{
  font-size:2.5rem;
  color:#555;
  line-height:1.5;
}}

/* -------- Footer -------- */
footer {{
  display:flex;
  justify-content:center;
  align-items:center;
  font-size:1.5rem;
  color:#fff;
}}
</style>
</head>

<body>
  <!-- Header -->
  <header>
    <div class="logo">SAFETY<span class="cross">+</span>FIRST</div>
  </header>

  <!-- Main -->
  <main>
    <section class="card">
      <h2>無災害継続日数(TCIR)</h2>
      <div class="counter">{working_days:,}<small>日</small></div>

      <div class="date-box">
        {start_date.year}年{start_date.month}月{start_date.day}日起算<br>
        {today.year}年{today.month}月{today.day}日現在
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer>TML 環境安全企画推進部</footer>
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