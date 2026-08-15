import streamlit as st
from datetime import date
from uuid import uuid4

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
# TOTAL XP
# --------------------

total_xp = sum(
    item["xp"]
    for item in st.session_state.quests
)

st.metric("⭐ TOTAL XP", total_xp)


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
    