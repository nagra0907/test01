import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 OpenAI 키 불러오기
load_dotenv()
openai.api_key = os.getenv("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")

st.set_page_config(page_title="GPT Q&A", page_icon="🤖")
st.title("💬 GPT-4 Q&A")
st.write("OpenAI GPT API를 이용한 질문 응답 서비스입니다.")

# 사용자 입력
question = st.text_input("무엇이든 질문해보세요:") 

# 버튼 클릭 시 GPT 호출
if st.button("답변 받기") and question:
    with st.spinner("GPT가 생각 중입니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",  # 또는 "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "당신은 친절한 AI 비서입니다."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response['choices'][0]['message']['content']
            st.success("GPT의 답변:")
            st.write(answer)
        except Exception as e:
            st.error(f"에러 발생: {e}")

