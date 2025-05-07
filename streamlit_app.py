import streamlit as st
from openai import OpenAI
import sys
import io

# UTF-8 인코딩 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

st.title("GPT-4.0 Mini Chatbot")

api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")
if api_key:
    st.session_state["api_key"] = api_key
elif "api_key" in st.session_state:
    api_key = st.session_state["api_key"]

question = st.text_input("질문을 입력하세요:")

@st.cache_data
def ask_gpt(prompt, key):
    try:
        client = OpenAI(api_key=key)
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
