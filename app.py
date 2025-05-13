import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import FAISS
import os

# 환경변수로 API Key 관리
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.title("📄 ChatPDF: PDF와 대화하기 (GitHub 버전)")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)

    st.session_state.vectorstore = vectorstore
    st.success(f"✅ '{uploaded_file.name}' 파일을 분석했습니다. 질문을 입력하세요.")

if st.button("Clear"):
    st.session_state.vectorstore = None
    st.success("벡터 스토어를 초기화했습니다.")

if st.session_state.vectorstore:
    question = st.text_input("질문을 입력하세요:", placeholder="예: 이 논문의 핵심 기여는?")
    if question:
        docs = st.session_state.vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        llm = ChatOpenAI(temperature=0)
        prompt = f"""당신은 PDF 문서의 도우미입니다. 아래 문서를 참고하여 질문에 답하세요.

문서 내용:
{context}

질문:
{question}

답변:"""

        response = llm.invoke(prompt)
        st.write("💡 답변:", response.content)
