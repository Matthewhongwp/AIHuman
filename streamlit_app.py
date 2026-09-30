"""
streamlit_app.py - Streamlit Community Cloud 배포용
------------------------------------------------------
어록 기반 인물 페르소나 챗봇의 웹 버전입니다.
Streamlit Community Cloud는 완전 무료로 GitHub 저장소를
바로 웹앱으로 배포해줍니다.

API 키는 코드에 넣지 않고, Streamlit Cloud의 "Secrets"에
ANTHROPIC_API_KEY 라는 이름으로 등록해서 사용합니다.
"""

import json
import os

import anthropic
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

# ---- 여기 두 줄만 원하는 인물/파일로 바꾸면 됩니다 ----
PERSON_NAME = "이건희"
QUOTES_PATH = "data/quotes.json"
# ------------------------------------------------

st.set_page_config(page_title=f"{PERSON_NAME} 페르소나 챗봇", page_icon="💬")


@st.cache_resource(show_spinner="모델과 어록 데이터를 불러오는 중입니다... (처음 접속 시 1~2분 소요)")
def load_resources():
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    if not quotes:
        raise ValueError("어록 데이터가 비어 있습니다. data/quotes.json 을 확인하세요.")

    model = SentenceTransformer("jhgan/ko-sroberta-multitask")
    texts = [q["text"] for q in quotes]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return quotes, model, embeddings


def get_api_key():
    # 1순위: Streamlit Secrets (배포 시 Settings > Secrets 에서 등록)
    if "ANTHROPIC_API_KEY" in st.secrets:
        return st.secrets["ANTHROPIC_API_KEY"]
    # 2순위: 로컬 실행 시 환경변수
    return os.environ.get("ANTHROPIC_API_KEY")


def search_top_k(model, embeddings, quotes, query: str, k: int = 5):
    query_vec = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
    scores = embeddings @ query_vec
    top_idx = np.argsort(-scores)[:k]
    return [quotes[i] for i in top_idx]


def build_system_prompt(retrieved):
    quotes_block = "\n".join(
        f"- ({q['topic']}, {q['source']}) {q['text']}" for q in retrieved
    )
    return f"""당신은 '{PERSON_NAME}'의 사고방식과 화법을 참고하여 답변을 생성하는 AI입니다.

아래는 질문과 관련성이 높다고 검색된 '{PERSON_NAME}'의 실제 어록 일부입니다:
{quotes_block}

지침:
1. 위 어록들의 논조, 가치관, 표현 방식(말투)을 참고해서 '{PERSON_NAME}'이라면 이 질문에 어떻게 답했을지 '추정'하여 새로 작성하세요.
2. 어록 원문을 그대로 인용하지 말고, 관점과 스타일만 반영해 직접 문장을 구성하세요.
3. 확실하지 않은 부분은 단정하지 말고 완곡하게 표현하세요.
4. 답변 마지막 줄에 반드시 다음 문구를 그대로 포함하세요:
   "※ 이 답변은 AI가 기존 발언 스타일을 참고해 추정한 것이며, 실제 {PERSON_NAME}의 발언이 아닙니다." """


def main():
    st.title(f"💬 {PERSON_NAME} 페르소나 챗봇")
    st.caption(f"'{PERSON_NAME}'의 실제 어록을 참고해 AI가 답변 스타일을 추정합니다. 실제 발언이 아닙니다.")

    api_key = get_api_key()
    if not api_key:
        st.error(
            "ANTHROPIC_API_KEY 가 설정되어 있지 않습니다. "
            "Streamlit Cloud의 Settings > Secrets 에서 등록해주세요."
        )
        st.stop()

    client = anthropic.Anthropic(api_key=api_key)
    quotes, model, embeddings = load_resources()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("질문을 입력하세요")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하는 중..."):
                retrieved = search_top_k(model, embeddings, quotes, question)
                system_prompt = build_system_prompt(retrieved)
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": question}],
                )
                answer = "".join(block.text for block in response.content if block.type == "text")
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
