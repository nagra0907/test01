import streamlit as st
import openai

# Streamlit 앱 제목 설정
st.title("💬 GPT-4 Chatbot")

# OpenAI API 키 입력 받기
api_key = st.text_input("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", type="password")

# 사용자 입력 받기
prompt = st.text_area("Ask a question:")

# "Ask!" 버튼 클릭 시 응답 생성
if st.button("Ask!") and api_key and prompt:
    try:
        # OpenAI API 키 설정
        openai.api_key = api_key

        # ChatCompletion API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # 응답 출력
        st.write("**Answer:**")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {e}")
