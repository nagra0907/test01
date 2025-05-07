import streamlit as st
from openai import OpenAI

st.title("GPT-4.0 Mini Chatbot")

api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# 세션에 저장
if api_key:
    st.session_state["api_key"] = api_key
elif "api_key" in st.session_state:
    api_key = st.session_state["api_key"]

question = st.text_input("질문을 입력하세요:")

@st.cache_data(show_spinner="GPT-4.0 mini에게 질문 중입니다...")
def ask_gpt(prompt, key):
    try:
        client = OpenAI(api_key=key)  # ⬅️ 반드시 인스턴스로 초기화
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러 발생: {e}"

if question:
    answer = ask_gpt(question, api_key)
    st.markdown("### 💬 GPT 응답")
    st.write(answer)
