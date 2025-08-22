import streamlit as st
import google.generativeai as genai
import os

# --- 画面のタイトル設定 ---
st.set_page_config(page_title="Gemini Chat Demo", page_icon="♊")
st.title("♊ Gemini API Chat Demo")
st.caption("Streamlit Community Cloudでデプロイしたデモアプリです。")

# --- APIキーの安全な設定 ---
# 【重要】Streamlit Community CloudのSettings > Secretsに "GEMINI_API_KEY" = "ご自身のAPIキー" を設定してください。
# ローカルで実行する場合は、環境変数にGEMINI_API_KEYを設定してください。
try:
    # st.secretsから "GEMINI_API_KEY" というキーで値を取得
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    # secretsにキーが存在しない場合のエラー処理
    st.error("⚠️ Gemini APIキーが設定されていません。")
    st.info("Streamlit Community CloudのSecretsに `GEMINI_API_KEY` を設定してください。")
    st.stop() # APIキーがない場合はここで処理を停止
except Exception as e:
    # その他のエラー（例: APIキーが無効など）
    st.error(f"APIキーの設定中にエラーが発生しました: {e}")
    st.stop()

# --- モデルの選択 ---
# model_name = "gemini-1.5-pro-latest" # 最新の軽量モデル
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)

# --- チャットセッションの初期化 ---
# st.session_stateにチャットオブジェクトがなければ、新たに作成します。
# これにより、ページを再読み込みしても会話の履歴が維持されます。
if "chat" not in st.session_state:
    # model.start_chat()で、会話履歴を保持するチャットセッションを開始します。
    st.session_state.chat = model.start_chat(history=[])

# --- チャット履歴の表示 ---
# st.session_state.chat.history には、これまでのすべてのやり取りが保存されています。
for message in st.session_state.chat.history:
    # roleに応じて 'user' または 'model' のチャットメッセージとして表示します。
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# --- ユーザーからの入力 ---
prompt = st.chat_input("メッセージを入力してください...")

if prompt:
    # ユーザーのメッセージをチャット履歴として表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIの応答を生成・表示
    with st.chat_message("model"):
        try:
            # st.session_state.chat.send_message() を使うことで、
            # これまでの会話履歴をすべて考慮した応答をAIが生成します。
            response = st.session_state.chat.send_message(prompt)
            
            # 応答がブロックされた場合の安全対策
            if not response.parts:
                st.warning("応答がブロックされました。別の表現で試してください。")
            else:
                response_text = response.text
                st.markdown(response_text)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")


