# MyAgent

아래 내용은 본 프로젝트를 수행하기 위한 계획 및 가이드입니다.
나중에 참고하여 다시 프로젝트를 진행할 수 있도록 정리했습니다.

## 1. 요구사항 정의

* **Agent 역할**
  * 파일시스템 관련 작업(읽기·쓰기·삭제·이동)만 수행
* **플랫폼**
  * 웹 기반 채팅 인터페이스
  * 대화 히스토리 영구 저장 및 조회
* **모델 호출**
  * OpenAI Chat Completion API (gpt-4o 또는 gpt-4) 사용
* **기술 스택**
  * Backend: Python + FastAPI
  * Agent 로직: LangGraph (Nodes·Edges 이용)
  * LLM 호출: `openai` Python SDK
  * DB: SQLite or MongoDB (채팅 기록 저장)
  * Frontend: React + WebSocket/REST

## 2. 환경 설정

1. **프로젝트 초기화**
   * Git, 가상환경(pyenv/venv) 설정
2. **의존성 설치**
   ```bash
   pip install fastapi uvicorn langgraph pydantic openai pymongo
   ```
3. **폴더 구조 설계**
   ```
   /project-root
     ├─ backend/
     │    ├─ app.py
     │    ├─ agents/
     │    │    ├─ filesystem_agent.py
     │    │    └─ llm_client.py
     │    ├─ models/
     │    └─ utils/
     ├─ frontend/
     └─ data/  (채팅 로그 저장)
   ```

## 3. LangGraph + ChatGPT API 기반 Agent 개발

1. **State 모델 정의**
   * `ChatState`:
     ```python
     class ChatState(TypedDict):
         history: List[Dict[str, str]]  # [{role: 'user'/'assistant', content: ...}, …]
         last_command: str               # 파싱된 파일시스템 명령
     ```
2. **LLM 클라이언트 (`llm_client.py`)**
   ```python
   import os
   import openai

   openai.api_key = os.getenv("OPENAI_API_KEY")

   def call_chatgpt(messages: List[Dict[str,str]]) -> str:
       resp = openai.ChatCompletion.create(
           model="gpt-4",
           messages=messages,
           temperature=0.2,
       )
       return resp.choices[0].message.content
   ```
3. **Node 구현**
   * **IntentParsingNode**
     * 입력: 최신 사용자 메시지
     * 처리: `call_chatgpt`로 “파일시스템 작업 요청인지 파싱”
     * 출력: `ChatState.last_command`에 “read:/path/to/file” 등 저장
   * **ExecuteFSNode**
     * 입력: `last_command`
     * 처리: Python 내장 `os`, `pathlib`으로 실제 FS 작업
     * 출력: 작업 결과 텍스트
   * **RespondNode**
     * 입력: FS 작업 결과 + 전체 `history`
     * 처리: `call_chatgpt`로 “친절한 안내 메시지” 생성
     * 출력: Assistant 응답 메시지
4. **Edge 구현**
   * 사용자 → IntentParsingNode → ExecuteFSNode → RespondNode → 사용자
5. **워크플로우 조립 & 테스트**
   ```python
   graph = Graph(
       initial_state=ChatState(history=[], last_command=""),
       nodes=[IntentParsingNode, ExecuteFSNode, RespondNode],
       edges=[...],
   )
   ```

## 4. 웹 채팅 인터페이스 구축

1. **Backend API**
   * **POST** `/chat/send`
     1. `state.history.append({"role":"user","content":msg})`
     2. `response = graph.run(state)`
     3. 결과 저장 후 JSON 반환
   * **GET** `/chat/history` → 전체 `state.history` 반환
2. **WebSocket (선택)**
   * `/ws/chat` → 실시간 메시지 주고받기
3. **Frontend (React)**
   * 입력창, 메시지 리스트 컴포넌트
   * `axios` 또는 `socket.io-client`로 Backend 연동
   * 페이지 로드시 `/chat/history`로 초기 로드

## 5. 테스트 및 검증

* **단위 테스트**
  * `llm_client.call_chatgpt` 모킹하여 Node 로직 검증
  * FS 작업 노드별 실제/모의 디렉토리 검증
* **통합 테스트**
  * FastAPI TestClient로 `/chat/send` 플로우 전체 검증
* **E2E 시나리오**
  1. “파일 목록 보여줘”
  2. “새 파일 생성해줘”
  3. “파일 내용 읽어줘”

## 6. 배포 및 운영

1. **Docker**
   * `backend/Dockerfile` & `frontend/Dockerfile` 작성
2. **CI/CD**
   * GitHub Actions: lint → test → build → deploy
3. **호스팅**
   * AWS ECS / Heroku / Vercel 등
4. **모니터링**
   * 에러 로깅(Sentry), API 호출 모니터링

## 7. 향후 확장

* 사용자 인증(API 키, OAuth)
* 권한별 FS 접근 제어
* 추가 툴 통합(e.g. Git CLI, DB)
* 세션별 멀티테넌시 지원

---

이제, OpenAI API 키 설정과 `llm_client` 코드부터 시작해 보시면 좋겠습니다. 추가 조정이나 궁금한 점 알려주세요!

## 8. 실행 및 테스트

아래 명령으로 백엔드와 프런트엔드를 실행하고, 기능을 검증할 수 있습니다.

### 1) 백엔드 실행
1. 가상환경 활성화 및 의존성 설치
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 환경변수 설정 (`.env` 파일 또는 export)
   ```env
   OPENAI_API_KEY=sk-<YOUR_KEY>
   ```
3. 서버 시작 (디폴트: http://127.0.0.1:8000)
   ```bash
   python -m uvicorn backend.app:app --reload
   ```

### 2) 프런트엔드 실행
1. Node.js 환경에서 패키지 설치
   ```bash
   cd frontend
   npm install    # 또는 yarn install
   ```
2. 개발 서버 시작 (http://localhost:5173)
   ```bash
   npm run dev    # 또는 yarn dev
   ```

### 3) 테스트 스크립트 실행
프로젝트 루트에서 Python 테스트 클라이언트 사용
```bash
# venv가 활성화된 쉘에서
python test_client.py
```
`test_client.py`가 차례대로 list, write, read, move, delete 기능을 호출하고 결과를 출력합니다.