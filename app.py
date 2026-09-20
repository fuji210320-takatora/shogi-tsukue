import streamlit as st

# ページ設定
st.set_page_config(page_title="机の使用状況マップ", layout="wide")

# 全員で状態を共有するための設定 (サーバーのメモリ上に保存)
@st.cache_resource
def get_desks():
    # id: 1~13, 状態: False(空席) / True(使用中)
    return {str(i): False for i in range(1, 14)}

desks = get_desks()

# ボタンが押されたときの処理
def toggle_desk(desk_id):
    desks[desk_id] = not desks[desk_id]

st.title("机の使用状況マップ")
st.write("ボタンを押すと「空席／使用中」が切り替わります。")

# 画面のレイアウト (5列に分割)
col1, col2, col3, col4, col5 = st.columns(5)

# 机のボタンを描画する関数
def draw_desk(col, desk_id, label):
    is_used = desks[desk_id]
    if is_used:
        status = "🔴 使用中"
    else:
        status = "🟢 空席"
        
    # ボタンを表示
    col.button(f"{label}\n\n{status}", key=f"btn_{desk_id}", on_click=toggle_desk, args=(desk_id,), use_container_width=True)

with col1:
    st.markdown("### 1列目")
    draw_desk(col1, '1', '将棋')
    draw_desk(col1, '2', '将棋')
    draw_desk(col1, '3', '将棋')

with col2:
    st.markdown("### 2列目")
    draw_desk(col2, '4', '将棋')
    draw_desk(col2, '5', '将棋')
    draw_desk(col2, '6', '将棋')

with col3:
    st.markdown("### 3列目")
    draw_desk(col3, '7', '将棋')
    draw_desk(col3, '8', '将棋')
    draw_desk(col3, '9', '将棋')

with col4:
    st.markdown("### 4列目")
    draw_desk(col4, '10', '将棋 (前)')
    draw_desk(col4, '11', 'オセロ')
    draw_desk(col4, '12', '囲碁')
    draw_desk(col4, '13', '将棋 (後)')

with col5:
    st.markdown("### 受付列")
    st.info("受付スペース")

st.markdown("---")
# Streamlitは自動更新されないため、他の人が変更した状態を見るためのボタン
st.button("🔄 最新の状態に更新", use_container_width=True)
