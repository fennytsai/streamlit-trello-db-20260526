import streamlit as st
import pandas as pd
import uuid
from streamlit_gsheets import GSheetsConnection

# =========================
# Page Config
# =========================
st.set_page_config(layout="wide")
st.title("🔥 Trello 看板完整版（卡片編輯 + 刪除 + Google Sheets）")

# =========================
# 連線
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Tasks", ttl=0)

# =========================
# 保證 ID 存在（超重要）
# =========================
if "id" not in df.columns:
    df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

# =========================
# 儲存函數（統一出口）
# =========================
def save_data(dataframe):
    conn.update(worksheet="Tasks", data=dataframe)
    st.cache_data.clear()
    st.rerun()

# =========================
# 卡片編輯 Dialog（Trello 核心）
# =========================
@st.dialog("✏️ 編輯任務")
def edit_task(task_id):

    task = df[df["id"] == task_id].iloc[0]

    new_title = st.text_input("任務名稱", task["title"])
    new_owner = st.text_input("負責人", task["owner"])

    new_status = st.selectbox(
        "狀態",
        ["To Do", "In Progress", "Done"],
        index=["To Do", "In Progress", "Done"].index(task["status"])
    )

    if st.button("💾 儲存修改"):
        df.loc[df["id"] == task_id, "title"] = new_title
        df.loc[df["id"] == task_id, "owner"] = new_owner
        df.loc[df["id"] == task_id, "status"] = new_status

        save_data(df)

# =========================
# 刪除任務
# =========================
def delete_task(task_id):
    global df
    df = df[df["id"] != task_id]
    save_data(df)

# =========================
# 新增任務
# =========================
st.write("### 🧠 新增任務")

with st.form("add_task", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        title = st.text_input("任務名稱")

    with c2:
        status = st.selectbox("狀態", ["To Do", "In Progress", "Done"])

    with c3:
        owner = st.text_input("負責人")

    submit = st.form_submit_button("新增")

if submit and title and owner:

    new_row = pd.DataFrame([{
        "id": str(uuid.uuid4()),
        "title": title,
        "status": status,
        "owner": owner
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

st.write("---")

# =========================
# 看板渲染
# =========================
st.write("### 📊 Trello 看板")

col1, col2, col3 = st.columns(3)

def render_board(status, col, color):

    with col:
        st.markdown(f"### {color} {status}")

        tasks = df[df["status"] == status]

        if tasks.empty:
            st.info("沒有任務")
            return

        for _, row in tasks.iterrows():

            with st.container(border=True):

                # 任務內容
                st.write(f"**{row['title']}**")
                st.caption(f"👤 {row['owner']}")

                # 操作按鈕
                c1, c2 = st.columns(2)

                with c1:
                    if st.button("✏️ 編輯", key=f"edit_{row['id']}"):
                        edit_task(row["id"])

                with c2:
                    if st.button("🗑 刪除", key=f"del_{row['id']}"):
                        delete_task(row["id"])

# 三欄
render_board("To Do", col1, "🔴")
render_board("In Progress", col2, "🟠")
render_board("Done", col3, "🟢")
