# 인물 페르소나 챗봇 - 웹 배포용 (Streamlit Community Cloud)

Hugging Face Spaces의 Gradio SDK가 유료(Pro)로 바뀌면서, 완전 무료인
**Streamlit Community Cloud**로 대신 배포하는 버전입니다.

## 폴더 구성
```
persona_bot_streamlit/
├── streamlit_app.py    # 웹 챗봇 코드 (Streamlit)
├── requirements.txt    # 필요한 패키지 목록
└── data/
    └── quotes.json      # 어록 데이터
```

## 배포 순서

### 1. GitHub 계정 만들기
https://github.com/join 에서 무료 가입합니다. (이미 있으면 생략)

### 2. 새 저장소(Repository) 만들기
1. GitHub 로그인 후 우측 상단 "+" → "New repository" 클릭
2. Repository name: 원하는 이름 (예: persona-bot)
3. **Public**으로 설정 (Streamlit 무료 플랜은 공개 저장소만 지원)
4. "Create repository" 클릭

### 3. 파일 업로드
1. 방금 만든 저장소 페이지에서 "Add file" → "Upload files" 클릭
2. `streamlit_app.py`, `requirements.txt` 를 끌어다 놓기
3. `data` 폴더를 만들려면, 업로드 화면에서 파일명을 `data/quotes.json` 라고
   직접 입력하면 자동으로 폴더가 생깁니다.
4. 아래 "Commit changes" 클릭

### 4. Streamlit Community Cloud에서 배포
1. https://share.streamlit.io 접속 → "Sign in with GitHub" 로 로그인
2. "Create app" 또는 "New app" 클릭
3. 방금 만든 저장소, 브랜치(main), 메인 파일 경로(`streamlit_app.py`) 선택
4. "Deploy" 클릭

### 5. API 키 등록 (Secrets)
1. 배포된 앱 페이지에서 우측 하단 "⋯" (점 3개) 메뉴 → "Settings" 클릭
2. "Secrets" 탭으로 이동
3. 아래처럼 입력:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-본인의-키-붙여넣기"
   ```
4. 저장하면 앱이 자동으로 재시작됩니다.

### 6. 완료!
1~3분 후 `https://본인아이디-persona-bot-xxxx.streamlit.app` 같은 주소가
생성됩니다. 이 링크를 아무에게나 공유하면 바로 브라우저에서 사용할 수 있습니다.

## 다른 인물로 바꾸고 싶다면
`streamlit_app.py` 상단의 이 두 줄만 수정하면 됩니다:
```python
PERSON_NAME = "이건희"
QUOTES_PATH = "data/quotes.json"
```

## 무료 한도 및 주의사항
- 앱당 메모리 약 1GB, CPU는 공유 자원입니다. 지금 프로그램 정도면 충분합니다.
- 오래 방문자가 없으면 앱이 자동으로 잠들며(슬립), 다음 접속 시 30~60초 정도
  깨어나는 시간이 걸릴 수 있습니다. 정상입니다.
- **공개 저장소만 무료**입니다. 비공개 저장소로 배포하려면 유료 플랜이 필요합니다.
- 질문에 답할 때마다 나가는 **Claude API 요금은 별도**로, Secrets에 등록한
  본인 키로 청구됩니다. Anthropic 콘솔에서 사용량 한도를 꼭 설정해두세요.
- 실존 인물의 어록을 기반으로 한 서비스이니, "AI의 추정 답변"이라는 문구가
  화면에 항상 보이도록 유지하세요 (코드에 이미 포함되어 있습니다).
