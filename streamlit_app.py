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

# すでに登録済みのQuestにIDやstatusがなければ追加
for item in st.session_state.quests:
    if "id" not in item:
        item["id"] = str(uuid4())

    if "status" not in item:
        item["status"] = "ACTIVE"

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

if st.button("START QUEST"):
    if quest:
        new_quest = {
            "id": str(uuid4()),
            "name": quest,
            "date": quest_date.isoformat(),
            "category": category,
            "status": "ACTIVE"
        }

        st.session_state.quests.append(new_quest)
        st.success(f"QUEST ADDED: {quest}")

    else:
        st.warning("クエストを入力してください！")

# --------------------
# MY QUESTS
# --------------------

st.divider()
st.subheader("⚔️ MY QUESTS")

if st.session_state.quests:

    for item in st.session_state.quests:

        st.write(f"**{item['name']}**")

        # Status表示
        if item["status"] == "COMPLETE":
            st.success("✅ COMPLETE")
        else:
            st.info("🎯 ACTIVE")

        st.caption(
            f"📅 {item['date']}　｜　{item['category']}"
        )

        # ACTIVEのQuestだけCOMPLETEボタンを表示
        if item["status"] == "ACTIVE":
            if st.button(
                "✅ COMPLETE",
                key=f"complete_{item['id']}"
            ):
                item["status"] = "COMPLETE"
                st.rerun()

        # 編集ボタン
        if st.button(
            "✏️ EDIT",
            key=f"edit_{item['id']}"
        ):
            st.session_state.editing_id = item["id"]
            st.rerun()

        # このQuestを編集中なら編集欄を表示
        if st.session_state.editing_id == item["id"]:

            st.write("### EDIT QUEST")

            edit_name = st.text_input(
                "Quest Name",
                value=item["name"],
                key=f"name_{item['id']}"
            )

            edit_date = st.date_input(
                "Date",
                value=date.fromisoformat(item["date"]),
                key=f"date_{item['id']}"
            )

            category_index = (
                CATEGORIES.index(item["category"])
                if item["category"] in CATEGORIES
                else 0
            )

            edit_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=category_index,
                key=f"category_{item['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "💾 SAVE CHANGES",
                    key=f"save_{item['id']}"
                ):
                    item["name"] = edit_name
                    item["date"] = edit_date.isoformat()
                    item["category"] = edit_category

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
    st.write("まだQuestはありません。")
    