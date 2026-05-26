import streamlit as st

# 導入服務帳戶連接核心套件
from streamlit_gsheets import GSheetsConnection

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
