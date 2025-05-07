import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="국립부경대학교 도서관 챗봇", layout="centered")

# --- 도서관 규정 요약 ---
PKNU_LIB_RULES_SUMMARY = """
  국립부경대학교 도서관 규정 요약

■ 목적 및 임무
- 도서관은 학술정보자료의 수집·정리·제공을 통해 연구와 교육을 지원함.

■ 조직 및 운영
- 도서관장은 2년 임기이며, 발전계획은 5년 단위 수립.
- 운영위원회 존재, 세부사항은 관장이 정함.

■ 직원 및 교육
- 사서 및 전산직원 배치, 연간 교육 이수 필요.

■ 자료 수집 및 관리
- 자료 유형: 단행본, 연속간행물, 전자자료 등.
- 장서 기준: 학생 1인당 70권, 연간 2권 증가 권장.
- 다양한 자료 수집 방식 존재 (수증, 교환 등).
- 기증 자료 문고 설치 가능, 자료 폐기 가능.

■ 시설 및 이용
- 1인당 1.2㎡ 시설 확보 권장.
- 이용 자격: 교직원, 학생, 허가된 외부인.
- 개관/휴관일은 관장이 정함.

■ 대출 및 반납
- 전임교원: 50권/90일, 학부생: 10권/14일.
- 전자책: 5권/5일.
- 일부 자료는 대출 제한(참고자료, 귀중자료 등).
- 반납 지연 시 대출 제한 및 변상 규정 있음.

■ 기타
- 자료의 비치, 관리, 반납 절차 존재.
- 질서 위반 시 이용 중지 가능, 개인정보 보호 의무.
"""

# --- 세션 상태 초기화 ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- 사이드바: API 키 및 Clear 버튼 ---
st.sidebar.header("🔐 OpenAI API 설정")
st.session_state.api_key = st.sidebar.text_input("API Key 입력", type="password", value=st.session_state.api_key)

if st.sidebar.button("🗑️ Clear 대화"):
    st.session_state.chat_history = []
    st.session_state.user_input = ""
    st.success("✅ 대화가 초기화되었습니다.")

# --- 페이지 제목 ---
st.title("📚 국립부경대학교 도서관 챗봇")

# --- 사용자 질문 입력 ---
st.session_state.user_input = st.text_input("도서관에 대해 궁금한 점을 입력하세요:", value=st.session_state.user_input)

# --- GPT 응답 함수 ---
def get_gpt_response(api_key, messages):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

# --- 질문 전송 ---
if st.button("전송") and st.session_state.user_input.strip():
    user_msg = {"role": "user", "content": st.session_state.user_input}
    st.session_state.chat_history.append(user_msg)

    system_msg = {
        "role": "system",
        "content": f"""
너는 국립부경대학교 도서관 규정에 따라 질문에 답하는 챗봇이다. 다음 규정 요약을 참고하라:

\"\"\"{PKNU_LIB_RULES_SUMMARY}\"\"\"

규정에 없는 질문에는 "규정에 해당 정보가 없습니다."라고만 답변하라.
"""
    }

    full_messages = [system_msg] + st.session_state.chat_history
    assistant_reply = get_gpt_response(st.session_state.api_key, full_messages)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    st.session_state.user_input = ""

# --- 대화 내용 출력 ---
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**🙋 사용자:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 챗봇:** {msg['content']}")

