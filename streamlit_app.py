import streamlit as st 

st.title("AY SIDE QUEST") 
st.write("EXPLORE WHO I CAN BECOME.")

st.divider()

st.subheader("NEW QUEST")

quest = st.text_input("What is your next quest?",
                      placeholder = "例:英会話レッスンに参加する"
                      )
category = st.selectbox(
    "Category",
    ["Adventure","Learning","Fitness","Social","Creative"]
)
if st.button("START QUEST"):
    if quest : 
        st.success(f"QUEST ADDED:{quest}")
        st.write(f"Category:{category}")
    else:
        st.warning("クエストを入力してください")    