import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드 (옵션)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 입력

st.title("💬 GPT-4 Q&A 앱")
st.write("OpenAI GPT-4 API를 사용한 Streamlit 앱입니다.")

# 사용자 입력
user_input = st.text_input("질문을 입력하세요:")

# 버튼 클릭 시 응답
if st.button("답변 받기") and user_input:
    with st.spinner("GPT가 생각 중입니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",  # 또는 "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "당신은 유용한 AI 비서입니다."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response['choices'][0]['message']['content']
            st.success("GPT의 답변:")
            st.write(answer)
        except Exception as e:
            st.error(f"에러 발생: {e}")
