
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存

system_prompt = """
与えられた文章を以下のルールにもとづいて[修正後]として修正案を提示してください。加えて、要点を[要点]として箇条書きで書きだしてください。
ルール：
・「いただく」は1文１か所とする
・受身形・自発系をなるべく使わない
・主語と述語の距離を短くする
・一文は長くても40字程度まで
・一文ごとに改行を入れる
"""


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("文章校正")
st.write("ChatGPT APIを使い文章の校正を行います。")

user_input = st.text_input("校正したい文章を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

# ---------- サイドバー ----------
st.sidebar.title("文章要約のルール")
rule = """
ルール：
・「いただく」は1文１か所とする
・受身形・自発系をなるべく使わない
・主語と述語の距離を短くする
・一文は長くても40字程度まで
・一文ごとに改行を入れる
"""

st.sidebar.write(rule.replace("\n", "<br>"), unsafe_allow_html=True)

