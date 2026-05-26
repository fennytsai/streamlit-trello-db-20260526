import streamlit as st
import pandas as pd
import uuid
from streamlit_gsheets import GSheetsConnection

# ======================
# 初始化
# ======================
st.set_page_config(layout="wide")
st.title("🔥 Trello 看板（卡片內編輯/刪除版）")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Tasks", ttl=0)

# ID 保護
if "id" not in df.columns:
    df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

# ======================
# 更新函數
# ======================
def save(df):
    conn.update(worksheet="Tasks", data=df)
    st.cache_data.clear()
    st.rerun()

# ======================
# 卡片編輯 Dialog
# ======================
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

        save(df)

# ======================
# 刪除函數
# ======================
def delete_task(task_id):
    global df
    df = df[df["id"] != task_id]
    save(df)

# ======================
# 看板
# ======================
col1, col2, col3 = st.columns(3)

def render_column(status, col, color):
    with col:
        st.markdown(f"### {color} {status}")

        tasks = df[df["status"] == status]

        if tasks.empty:
            st.info("無任務")
            return

        for _, row in tasks.iterrows():

            with st.container(border=True):

                st.write(f"**{row['title']}**")
                st.caption(f"👤 {row['owner']}")

                c1, c2 = st.columns(2)

                # ✏️ 編輯
                with c1:
                    if st.button("✏️", key=f"edit_{row['id']}"):
                        edit_task(row["id"])

                # 🗑 刪除
                with c2:
                    if st.button("🗑", key=f"del_{row['id']}"):
                        delete_task(row["id"])

# 三欄
render_column("To Do", col1, "🔴")
render_column("In Progress", col2, "🟠")
render_column("Done", col3, "🟢")
