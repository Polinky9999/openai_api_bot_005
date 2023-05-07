
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存

system_prompt = """
与えらえれた文章を要約してください。
箇条書きで出力してください。
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
st.title("文章要約")
st.write("ChatGPT APIを使った文章要約を行います。")

user_input = st.text_input("要約したい文章を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

# ---------- サイドバー ----------
st.sidebar.title("st.sidebar")

y = st.sidebar.slider("yの値")
st.sidebar.write(str(y) + "の2倍は" + str(y*2))

df_side = pd.DataFrame({
    "animal": ["犬", "猫", "兎", "象", "蛙"],
    "color": ["赤", "青", "黄", "白", "黒"]
    })
selected_side = st.sidebar.selectbox(
    "どの動物を選びますか？",
    df_side["animal"]
    )
st.sidebar.write("あなたは" + str(selected_side) + "を選びました！")
