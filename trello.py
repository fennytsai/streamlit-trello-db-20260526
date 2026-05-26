import streamlit as st

# 導入服務帳戶連接核心套件
from streamlit_gsheets import GSheetsConnection

import pandas as pd

st.caption("授權標註：edit by 闕河正 | 專屬資淺初學者講義")
# 1. 網頁初始化設定（必須放在程式碼第一行）
# layout="wide" 會把網頁兩邊的留白填滿，變成寬螢幕，最適合看多欄位的看板
st.set_page_config(layout="wide")
st.title("階段一：Trello 畫布空間規劃測試")

st.write("---")

# 2. 呼叫 st.columns(3)，在網頁橫向切出三個一模一樣寬度的大直欄變數
col1, col2, col3, col4 = st.columns(4)

# 3. 運用 with 語法，像填空一樣把文字塞進對應的直欄空間裡
with col1:
    st.markdown("### To Do (待辦)")
    st.write("這裡未來要放『待辦事項』的卡片")

with col2:
    st.markdown("### In Progress (執行中)")
    st.write("這裡未來要放『執行中』的卡片")

with col3:
    st.markdown("### Done (已完成)")
    st.write("這裡未來要放『已完成』的卡片")
    
with col4:
    st.markdown("### 備註")
    st.write("這裡未來要放『備註』的卡片")

st.set_page_config(layout="wide")
st.title("階段二：雲端資料庫讀取與原始表格分析")

# 1. 建立雲端連接器
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 從 Google 試算表讀取 "Tasks" 工作表
# 核心細節：ttl="0" 代表快取時間為 0 秒，強迫它每次重整都即時去雲端抓最新，不准用舊記憶
df = conn.read(worksheet="Tasks", ttl="0")

st.write("---")
st.write("### 這是從 Google 雲端硬碟抓回來的原始黑白表格（Bare Data）：")

# 3. 直接用 st.dataframe() 把整張表格原汁原味印在網頁上
st.dataframe(df)

# 4. 拆解底層資訊給學生看
st.write("經過 Python 分析，這張表格擁有的『直欄欄位名稱（Columns）』有：", list(df.columns))


st.set_page_config(layout="wide")
st.title("階段 2.5：DataFrame 數據單點座標拆解實驗")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Tasks", ttl="0")

st.write("### 目前的雲端原始表格：")
st.dataframe(df)

st.write("---")
st.write("### 精準座標抽離實驗：")

# 使用 .loc[行號, 欄位名] 精準抓取特定格子
first_title = df.loc[0, "title"]
first_owner = df.loc[0, "owner"]

st.write(f"機器人回報：我們發現第 0 列（第一行任務）的名稱是：**{first_title}**")
st.write(f"機器人回報：這一行的負責人是：**{first_owner}**")

st.set_page_config(layout="wide") 

st.title(" 階段三：外星文濾網分流與空間歸隊測試") 


conn = st.connection("gsheets", type=GSheetsConnection) 

df = conn.read(worksheet="Tasks", ttl="0")

st.write("---")

col1, col2, col3, col4 = st.columns(4)

with col1: 

    st.markdown("###  To Do") 

    #  內層做濾網，外層做篩選：只抓出狀態為 To Do 的小表格 

    todo_df = df[df["status"] == "To Do"] # 把它印在左邊這欄
    st.dataframe(todo_df)

with col2: 

    st.markdown("###  In Progress") 

    #  只抓出狀態為 In Progress 的小表格 

    ip_df = df[df["status"] == "In Progress"] 

    st.dataframe(ip_df)

with col3: 

    st.markdown("###  Done") 

    #  只抓出狀態為 Done 的小表格 

    done_df = df[df["status"] == "Done"] 

    st.dataframe(done_df)
    
with col4: 

    st.markdown("###  Remark") 

    #  只抓出狀態為 Remark 的小表格 

    done_df = df[df["status"] == "Remark"] 

    st.dataframe(done_df)


st.set_page_config(layout="wide")

st.title(" 階段 3.5：iterrows 迴圈解構點名現場實驗") 

conn = st.connection("gsheets", type=GSheetsConnection) 

df = conn.read(worksheet="Tasks", ttl="0")

todo_df = df[df["status"] == "To Do"]

st.write("---") 

st.write("###  進入 Python 迴圈自動化點名現場：")

for idx, row in todo_df.iterrows(): 

    # 每一圈，我們用一個小紅框（st.error）來代表一次巡迴 

    st.error(f" 迴圈巡邏：目前點名點到了第 {idx} 行的任務：") 
    
    st.write(row) 
    
    st.write(f" ➔ 【title 任務名稱】這一格拿到了： {row['title']}") 

    st.write(f" ➔ 【owner 負責人】這一格拿到了： {row['owner']}")
    # https://docs.streamlit.io/develop/api-reference/status/st.error
    st.info(f" ➔ 【status 任務狀態】這一格拿到了： {row['status']}")





st.set_page_config(layout="wide")

st.title(" 階段四終極完成版：GitHub 雲端同步 Trello 看板")

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Tasks", ttl="0")

# ==========================================

#  區塊一：上方新增任務輸入表單

# ==========================================

st.write("###  指派新任務")

with st.form("task_input_form", clear_on_submit=True):

    c_title, c_status, c_owner = st.columns([2, 1, 1]) # 運用權重比例切分表單

    with c_title:

        new_title = st.text_input(" 任務名稱", placeholder="輸入任務名稱...")

    with c_status:

        new_status = st.selectbox(" 狀態", ["To Do", "In Progress", "Done"])

    with c_owner:

        new_owner = st.text_input(" 負責人", placeholder="誰來負責...")

    

    submit_btn = st.form_submit_button("確認指派並同步雲端")

if submit_btn and new_title and new_owner:

    new_data = {"title": new_title, "status": new_status, "owner": new_owner}

    new_row = pd.DataFrame([new_data])

    #  核心安全：新版 Python 廢棄 .append()，在雲端必須改用 pd.concat() 進行表格拼接

    updated_df = pd.concat([df, new_row], ignore_index=True)

    conn.update(worksheet="Tasks", data=updated_df)

    st.success(" 資料已跨越限制，成功同步寫入 Google 試算表！")

    st.rerun() # 強制網頁自我重整，重新讀取，讓新卡片亮起來

st.write("---")

# ==========================================

#  區塊二：下方 Trello 三縱欄畫布與卡片渲染

# ==========================================
# ==========================================
# 區塊二：下方 Trello 三縱欄畫布與卡片渲染
# ==========================================

st.write("### 📋 看板動態狀態監控")

trello_col1, trello_col2, trello_col3 = st.columns(3)

status_map = {
    "To Do": trello_col1,
    "In Progress": trello_col2,
    "Done": trello_col3
}

color_map = {
    "To Do": "red",
    "In Progress": "orange",
    "Done": "green"
}

for status, column in status_map.items():

    with column:

        st.markdown(
            f"### <span style='color:{color_map[status]}'>{status}</span>",
            unsafe_allow_html=True
        )

        task_list = df[df["status"] == status]

        if not task_list.empty:

            for idx, row in task_list.iterrows():

                with st.container(border=True):

                    st.write(f"### {row['title']}")
                    st.caption(f"負責人：{row['owner']}")

                    # ==================================
                    # 狀態修改區
                    # ==================================

                    new_status = st.selectbox(
                        "修改狀態",
                        ["To Do", "In Progress", "Done"],
                        index=["To Do", "In Progress", "Done"].index(row["status"]),
                        key=f"status_{idx}"
                    )

                    # 如果狀態被修改
                    if new_status != row["status"]:

                        df.at[idx, "status"] = new_status

                        conn.update(
                            worksheet="Tasks",
                            data=df
                        )

                        st.success("任務狀態已更新！")

                        st.rerun()

                    # ==================================
                    # 刪除按鈕
                    # ==================================

                    if st.button(
                        "🗑️ 刪除任務",
                        key=f"delete_{idx}"
                    ):

                        # 刪除該列
                        df = df.drop(idx)

                        # 重新整理 index
                        df = df.reset_index(drop=True)

                        # 同步回 Google Sheets
                        conn.update(
                            worksheet="Tasks",
                            data=df
                        )

                        st.warning("任務已刪除")

                        st.rerun()

        else:

            st.info(f"目前沒有 {status} 任務")
