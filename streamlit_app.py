







import streamlit as st
from datetime import date
from uuid import uuid4
import gspread
from google.oauth2.service_account import Credentials
# Google Sheets 接続
@st.cache_resource
def connect_google_sheets():
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open("AY SIDE QUEST DATA")
    worksheet = spreadsheet.worksheet("シート1")

    return worksheet
# 接続テスト
try:
    worksheet = connect_google_sheets()
    st.success("✅ Google Sheets 接続成功！")
except Exception as e:
    st.error(f"Google Sheets 接続エラー: {e}")

# --------------------
# 基本設定
# --------------------

CATEGORIES = [
    "🏛 PUBLIC SERVICE",
    "🏃 ATHLETE",
    "🌏 EXPLORE",
    "🦖 CURIOSITY",
    "❤️ GIVE",
    "🤖 BUILD",
    "✍️ CREATE"
]

st.title("AY SIDE QUEST")
st.write("EXPLORE WHO I CAN BECOME.")

# --------------------
# Session State
# --------------------

if "quests" not in st.session_state:
    st.session_state.quests = []

if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

# 昔のQuestに新しい項目がなければ追加
for item in st.session_state.quests:

    if "id" not in item:
        item["id"] = str(uuid4())

    if "status" not in item:
        item["status"] = "ACTIVE"

    if "first_time" not in item:
        item["first_time"] = False

    if "solo" not in item:
        item["solo"] = False

    if "courage" not in item:
        item["courage"] = 1

    if "xp" not in item:
        item["xp"] = 0


# --------------------
# XP計算
# --------------------

def calculate_xp(item):

    xp = 10  # Quest COMPLETE

    if item["first_time"]:
        xp += 10

    if item["solo"]:
        xp += 10

    xp += item["courage"] * 2

    return xp

# --------------------
# LEVEL判定
# --------------------

def get_level(xp):

    if xp < 100:
        return 1, "ROOKIE", 0, 100

    elif xp < 250:
        return 2, "CURIOUS", 100, 250

    elif xp < 450:
        return 3, "ADVENTURER", 250, 450

    elif xp < 700:
        return 4, "EXPLORER", 450, 700

    elif xp < 1000:
        return 5, "CHALLENGER", 700, 1000

    elif xp < 1500:
        return 6, "CREATOR", 1000, 1500

    else:
        return 7, "WAYFINDER", 1500, None
    


# --------------------
# TOTAL XP
# --------------------

total_xp = sum(
    item["xp"]
    for item in st.session_state.quests
)

st.metric("⭐ TOTAL XP", total_xp)

# 現在のLEVELを計算
level, level_name, level_start, level_end = get_level(total_xp)

st.subheader(
    f"🧭 LEVEL {level} — {level_name}"
)

if level_end is not None:

    progress = (
        (total_xp - level_start)
        / (level_end - level_start)
    )

    st.progress(progress)

    st.caption(
        f"{total_xp} / {level_end} XP"
    )

else:

    st.progress(1.0)

    st.caption(
        f"{total_xp} XP — Highest Level"
    )

# --------------------
# GUIDE
# --------------------

with st.expander("ℹ️ AY SIDE QUEST GUIDE"):

    st.subheader("⭐ XP SYSTEM")

    st.write("""
    **Quest Complete**：+10 XP

    **First Time**：+10 XP

    **Solo Challenge**：+10 XP

    **Courage**
    - ★1：+2 XP
    - ★2：+4 XP
    - ★3：+6 XP
    - ★4：+8 XP
    - ★5：+10 XP
    """)

    st.divider()

    st.subheader("🔥 COURAGE GUIDE")

    st.write("""
    **★1 — COMFORT**  
    ほぼ緊張しない。いつもの範囲。気軽にできる。

    **★2 — SMALL STEP**  
    少し新しい。多少迷うけど、そこまで怖くない。

    **★3 — CHALLENGE**  
    ちょっと勇気が必要。行く前に少し緊張する。

    **★4 — OUTSIDE COMFORT ZONE**  
    かなり迷う・緊張する。でも挑戦してみたい。

    **★5 — BIG LEAP**  
    怖い・かなり不安。それでも自分から挑戦する。
    """)

    st.divider()

    st.subheader("🧭 LEVEL GUIDE")

    st.write("""
    **Lv.1 ROOKIE｜0–99 XP**  
    まず動き始めた。

    **Lv.2 CURIOUS｜100–249 XP**  
    新しいものへ手を伸ばし始めた。

    **Lv.3 ADVENTURER｜250–449 XP**  
    自分から未知の経験を選ぶようになった。

    **Lv.4 EXPLORER｜450–699 XP**  
    複数分野で継続的に世界を広げている。

    **Lv.5 CHALLENGER｜700–999 XP**  
    Comfort Zoneの外へ出る挑戦が増えている。

    **Lv.6 CREATOR｜1000–1499 XP**  
    経験するだけでなく、自分で何かを生み出している。

    **Lv.7 WAYFINDER｜1500 XP〜**  
    自分に合う生き方を、自分で選び育てている。
    """)

    st.divider()

    st.info(
        "XPはあなたの価値を測るものではありません。"
        "どれだけ試し、経験し、世界を広げたかを記録するものです。"
    )


# --------------------
# NEW QUEST
# --------------------

st.divider()
st.subheader("NEW QUEST")

quest = st.text_input(
    "What is your next quest?",
    placeholder="例：英会話レッスンに参加する"
)

quest_date = st.date_input(
    "Quest Date",
    value="today"
)

category = st.selectbox(
    "Category",
    CATEGORIES
)

first_time = st.checkbox(
    "✨ First time?"
)

solo = st.checkbox(
    "🧭 Solo challenge?"
)

courage = st.slider(
    "🔥 Courage",
    min_value=1,
    max_value=5,
    value=3
)

st.write("Courage:", "★" * courage + "☆" * (5 - courage))


if st.button("START QUEST"):

    if quest:

        new_quest = {
            "id": str(uuid4()),
            "name": quest,
            "date": quest_date.isoformat(),
            "category": category,
            "status": "ACTIVE",
            "first_time": first_time,
            "solo": solo,
            "courage": courage,
            "xp": 0
        }

        st.session_state.quests.append(new_quest)
        try:
            worksheet = connect_google_sheets()

            worksheet.append_row([
                new_quest["id"],
                new_quest["name"],
                new_quest["date"],
                new_quest["category"],
                new_quest["status"],
                new_quest["first_time"],
                new_quest["solo"],
                new_quest["courage"],
                new_quest["xp"],
            ])

            st.success("☁️ Google Sheetsにも保存しました！")

        except Exception as e:
            st.error(f"Google Sheets保存エラー: {e}")

        st.success(
            f"QUEST ADDED: {quest}"
        )

    else:
        st.warning(
            "クエストを入力してください！"
        )


# --------------------
# MY QUESTS
# --------------------

st.divider()
st.subheader("⚔️ MY QUESTS")

if st.session_state.quests:

    for item in st.session_state.quests:

        st.write(
            f"**{item['name']}**"
        )

        # Status
        if item["status"] == "COMPLETE":

            st.success("✅ COMPLETE")

            st.write(
                f"⭐ **+{item['xp']} XP**"
            )

        else:

            st.info("🎯 ACTIVE")

        # Quest情報
        st.caption(
            f"📅 {item['date']}　｜　{item['category']}"
        )

        st.caption(
            f"🔥 {'★' * item['courage']}{'☆' * (5 - item['courage'])}"
        )

        details = []

        if item["first_time"]:
            details.append("✨ FIRST TIME")

        if item["solo"]:
            details.append("🧭 SOLO")

        if details:
            st.caption(" ｜ ".join(details))


        # --------------------
        # COMPLETE
        # --------------------

        if item["status"] == "ACTIVE":

            if st.button(
                "✅ COMPLETE",
                key=f"complete_{item['id']}"
            ):

                item["status"] = "COMPLETE"

                item["xp"] = calculate_xp(
                    item
                )

                st.rerun()


        # --------------------
        # EDIT
        # --------------------

        if st.button(
            "✏️ EDIT",
            key=f"edit_{item['id']}"
        ):

            st.session_state.editing_id = item["id"]

            st.rerun()


        # --------------------
        # EDIT QUEST
        # --------------------

        if st.session_state.editing_id == item["id"]:

            st.write("### EDIT QUEST")

            edit_name = st.text_input(
                "Quest Name",
                value=item["name"],
                key=f"name_{item['id']}"
            )

            edit_date = st.date_input(
                "Date",
                value=date.fromisoformat(
                    item["date"]
                ),
                key=f"date_{item['id']}"
            )

            category_index = (
                CATEGORIES.index(
                    item["category"]
                )
                if item["category"] in CATEGORIES
                else 0
            )

            edit_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=category_index,
                key=f"category_{item['id']}"
            )

            edit_first_time = st.checkbox(
                "✨ First time?",
                value=item["first_time"],
                key=f"first_{item['id']}"
            )

            edit_solo = st.checkbox(
                "🧭 Solo challenge?",
                value=item["solo"],
                key=f"solo_{item['id']}"
            )

            edit_courage = st.slider(
                "🔥 Courage",
                min_value=1,
                max_value=5,
                value=item["courage"],
                key=f"courage_{item['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 SAVE CHANGES",
                    key=f"save_{item['id']}"
                ):

                    item["name"] = edit_name

                    item["date"] = (
                        edit_date.isoformat()
                    )

                    item["category"] = (
                        edit_category
                    )

                    item["first_time"] = (
                        edit_first_time
                    )

                    item["solo"] = edit_solo

                    item["courage"] = (
                        edit_courage
                    )

                    # COMPLETE済みなら
                    # XPも再計算
                    if item["status"] == "COMPLETE":

                        item["xp"] = calculate_xp(
                            item
                        )

                    st.session_state.editing_id = None

                    st.rerun()


            with col2:

                if st.button(
                    "CANCEL",
                    key=f"cancel_{item['id']}"
                ):

                    st.session_state.editing_id = None

                    st.rerun()

        st.divider()

else:

    st.write(
        "まだQuestはありません。"
    )

    
