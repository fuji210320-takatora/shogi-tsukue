import streamlit as st
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(page_title="机の使用状況", layout="wide")

# JST(日本時間)を取得する関数
def get_jst_time():
    return (datetime.utcnow() + timedelta(hours=9)).strftime("%H:%M")

# 全員で状態を共有するためのデータストア
@st.cache_resource
def get_desks():
    desks = {}
    
    # 1〜3列目 (各3つの将棋)
    for col in range(1, 4):
        for row in range(1, 4):
            desks[f"{col}-{row}"] = {"name": "将棋", "is_used": False, "time": None}
    
    # 4列目 (受付 + 将棋, オセロ, 囲碁, 将棋)
    desks["4-0"] = {"name": "受付", "is_used": False, "time": None, "is_reception": True}
    desks["4-1"] = {"name": "将棋", "is_used": False, "time": None}
    desks["4-2"] = {"name": "オセロ", "is_used": False, "time": None}
    desks["4-3"] = {"name": "囲碁", "is_used": False, "time": None}
    desks["4-4"] = {"name": "将棋", "is_used": False, "time": None}
    
    return desks

desks = get_desks()

# ボタンが押されたときの処理
def register_desk(desk_id):
    desks[desk_id]["is_used"] = True
    desks[desk_id]["time"] = get_jst_time()

def release_desk(desk_id):
    desks[desk_id]["is_used"] = False
    desks[desk_id]["time"] = None

# CSS（デザインと縦の間隔の定義）
st.markdown("""
<style>
.desk-container {
    border: 2px solid #ccc;
    border-radius: 8px;
    padding: 15px 10px;
    text-align: center;
    margin-bottom: 5px;
    transition: 0.3s;
}
.desk-white {
    background-color: #ffffff;
    color: #333333;
}
.desk-red {
    background-color: #ffeaea;
    border-color: #ff4c4c;
    color: #cc0000;
}
.desk-title {
    font-size: 20px;
    font-weight: bold;
}
.desk-time {
    font-size: 16px;
    height: 24px;
    margin-top: 5px;
    color: #555;
}
.desk-red .desk-time {
    color: #cc0000;
}
/* 左3列の縦の隙間を調整するクラス */
.spacer {
    height: 150px;
}
</style>
""", unsafe_allow_html=True)

# 画面上部
st.markdown("<h2 style='text-align: center;'>前</h2>", unsafe_allow_html=True)
st.markdown("---")

# 1つの机とその下のボタンを描画する関数
def draw_desk(desk_id):
    desk = desks[desk_id]
    
    # 受付用の特別デザイン
    if desk.get("is_reception"):
        st.markdown(f'''
        <div class="desk-container desk-white">
            <div class="desk-title">{desk["name"]}</div>
            <div class="desk-time"></div>
        </div>
        ''', unsafe_allow_html=True)
        st.write("") # ボタンがない分のスペース補正
        st.write("")
        return

    # 状態に応じて背景色と打刻テキストを決定
    bg_class = "desk-red" if desk["is_used"] else "desk-white"
    time_text = f"打刻: {desk['time']}" if desk["time"] else "未登録"

    # 四角形（状態表示）の描画
    st.markdown(f'''
    <div class="desk-container {bg_class}">
        <div class="desk-title">{desk["name"]}</div>
        <div class="desk-time">{time_text}</div>
    </div>
    ''', unsafe_allow_html=True)

    # 登録・解除ボタンを横並びで配置
    col1, col2 = st.columns(2)
    col1.button("登録", key=f"reg_{desk_id}", on_click=register_desk, args=(desk_id,), use_container_width=True)
    col2.button("解除", key=f"rel_{desk_id}", on_click=release_desk, args=(desk_id,), use_container_width=True)

# 4列のレイアウト枠を作成
cols = st.columns(4)

# 1〜3列目 (将棋 x 3) ＋ 間にスペースを追加
for col_idx in range(3):
    with cols[col_idx]:
        for row_idx in range(1, 4):
            draw_desk(f"{col_idx + 1}-{row_idx}")
            # 1つ目と2つ目の机の下に縦のスペースを入れる
            if row_idx < 3:
                st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# 4列目 (受付, 将棋, オセロ, 囲碁, 将棋)
with cols[3]:
    for i in range(0, 5):
        draw_desk(f"4-{i}")
        st.write("") # 少しだけ余白を入れる

# 画面下部
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>後ろ</h2>", unsafe_allow_html=True)

# Streamlitは自動更新されないため、他の人が変更した状態を見るためのボタン
st.button("🔄 画面を更新 (他の人の変更を反映)", use_container_width=True)
