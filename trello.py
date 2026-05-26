import streamlit as st
import pandas as pd
import uuid
from streamlit_gsheets import GSheetsConnection

# =========================
# Page
# =========================
st.set_page_config(layout="wide")
st.title("階段四：Trello + Google Sheets 穩定版")

# =========================
# 連線
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)

# ⚠️ 每次都抓最新（避免舊資料）
df = conn.read(worksheet="Tasks", ttl=0)

# =========================
# ID 保護（刪除必備）
# =========================
if "id" not in df.columns:
    df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

# =========================
# 新增任務
# =========================
st.write("### 🧠 指派新任務")

with st.form("task_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        new_title = st.text_input("任務名稱")

    with c2:
        new_status = st.selectbox("狀態", ["To Do", "In Progress", "Done"])

    with c3:
        new_owner = st.text_input("負責人")

    submit = st.form_submit_button("新增任務")

if submit and new_title and new_owner:

    new_row = pd.DataFrame([{
        "id": str(uuid.uuid4()),
        "title": new_title,
        "status": new_status,
        "owner": new_owner
    }])

    updated_df = pd.concat([df, new_row], ignore_index=True)

    conn.update(worksheet="Tasks", data=updated_df)

    st.success("已新增任務")
    st.cache_data.clear()
    st.rerun()

st.write("---")

# =========================
# 任務表（可編輯）
# =========================
st.write("### ✏️ 任務即時編輯（可改狀態）")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "status": st.column_config.SelectboxColumn(
            "status",
            options=["To Do", "In Progress", "Done"]
        )
    }
)

if st.button("💾 儲存所有修改"):
    conn.update(worksheet="Tasks", data=edited_df)
    st.success("已同步更新")
    st.cache_data.clear()
    st.rerun()

st.write("---")

# =========================
# 刪除任務
# =========================
st.write("### 🗑️ 刪除任務")

delete_ids = st.multiselect(
    "選擇要刪除的任務",
    df["id"],
    format_func=lambda x: df[df["id"] == x]["title"].values[0]
)

if st.button("刪除選取任務"):
    df = df[~df["id"].isin(delete_ids)]

    conn.update(worksheet="Tasks", data=df)

    st.success("已刪除")
    st.cache_data.clear()
    st.rerun()

st.write("---")

# =========================
# Trello 看板
# =========================
st.write("### 📊 Trello 看板")

col1, col2, col3 = st.columns(3)

# -------- To Do --------
with col1:
    st.markdown("### 🔴 To Do")

    todo = df[df["status"] == "To Do"]

    if not todo.empty:
        for _, row in todo.iterrows():
            with st.container(border=True):
                st.write(f"**{row['title']}**")
                st.caption(f"👤 {row['owner']}")
    else:
        st.info("無任務")

# -------- In Progress --------
with col2:
    st.markdown("### 🟠 In Progress")

    ip = df[df["status"] == "In Progress"]

    if not ip.empty:
        for _, row in ip.iterrows():
            with st.container(border=True):
                st.write(f"**{row['title']}**")
                st.caption(f"👤 {row['owner']}")
    else:
        st.info("無任務")

# -------- Done --------
with col3:
    st.markdown("### 🟢 Done")

    done = df[df["status"] == "Done"]

    if not done.empty:
        for _, row in done.iterrows():
            with st.container(border=True):
                st.write(f"~~**" + row['title'] + "**~~")
                st.caption(f"👤 {row['owner']}")
    else:
        st.info("無任務")
