import streamlit as st
import openai

st.title("GPT-4.0 Mini Chatbot")

# 🔑 OpenAI API 키 입력받기
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# Session에 API 키 저장
if api_key:
    st.session_state["api_key"] = api_key
elif "api_key" in st.session_state:
    api_key = st.session_state["api_key"]

# 사용자 질문 입력
question = st.text_input("무엇이든 질문해보세요:")

# GPT 호출 함수
@st.cache_data(show_spinner="GPT-4.0 mini에게 질문 중입니다...")
def ask_gpt(prompt, key):
    if not key:
        return "❗ API 키가 없습니다. 먼저 입력해주세요."
    try:
        openai.api_key = key
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # gpt-4.0 mini
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러 발생: {e}"

# 질문이 있을 경우 응답 출력
if question:
    answer = ask_gpt(question, api_key)
    st.markdown("### 💬 GPT 응답")
    st.write(answer)
