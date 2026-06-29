# AI 서버 API 명세

## 서버 실행

### 방법 1: ngrok 사용 (권장) ⭐
```bash
pip install pyngrok
python run_with_ngrok.py
```

자동으로 외부 URL이 생성되고, 백엔드에서 즉시 사용 가능합니다.

**출력 예시:**
```
🌐 Public URL: https://abcd-1234-5678-efgh.ngrok.io
🔗 로컬: http://localhost:8001
🔗 외부: https://abcd-1234-5678-efgh.ngrok.io
```

### 방법 2: 직접 실행
```bash
uvicorn ai.server:app --reload --host 0.0.0.0 --port 8001
```

- 로컬: `http://localhost:8001`
- 같은 네트워크: `http://<당신의_IP>:8001`
- 외부: `http://<공인_IP>:8001` (포트포워딩 필요시)

## 엔드포인트

### 1. 변명 생성
**POST** `/generate-excuses`

요청 본문:
```json
{
    "situation": "약속을 안 가고 싶어",
    "politeness": 7,
    "credibility": 5
}
```

응답:
```json
{
    "excuses": [
        {
            "text": "변명 내용",
            "reaction": "상대: 상대방의 반응",
            "grade": "A",
            "caution": "유의사항"
        },
        ...
    ]
}
```

**파라미터:**
- `situation` (string): 상황 (예: "약속", "과제", "회식")
- `politeness` (int): 정중함 (1-10, 1=막말, 10=존댓말)
- `credibility` (int): 신뢰도 (1-10, 1=누가 봐도 뻥, 10=안 들킴)

---

### 2. 디펜스 반응 생성
**POST** `/defense-reaction`

요청 본문:
```json
{
    "original_excuse": "몸이 안 좋아서 못 갈 것 같아",
    "opponent_reaction": "엄마: 또? 증빙 사진 보내줄래?",
    "user_defense": "지금 진짜 열이 나서 침대에 누워있어",
    "attempt_num": 1
}
```

응답:
```json
{
    "reaction": "상대방의 반응"
}
```

**파라미터:**
- `original_excuse` (string): 원래 변명
- `opponent_reaction` (string): 상대의 초기 반응
- `user_defense` (string): 사용자의 디펜스 말
- `attempt_num` (int): 시도 횟수 (1-3)

---

### 3. 의심도 측정
**POST** `/measure-suspicion`

요청 본문:
```json
{
    "original_excuse": "몸이 안 좋아서 못 갈 것 같아",
    "conversation_history": [
        {
            "user": "지금 진짜 열이 나서 침대에 누워있어",
            "opponent": "그런가... 어디 아파?"
        },
        {
            "user": "감기인 것 같아",
            "opponent": "그래, 빨리 나아"
        }
    ]
}
```

응답:
```json
{
    "suspicion": 45,
    "reason": "사용자의 설명이 일관되고 구체적이어서 충분히 설득력이 있음",
    "success": true
}
```

**파라미터:**
- `original_excuse` (string): 원래 변명
- `conversation_history` (array): 대화 기록
  - `user` (string): 사용자 말
  - `opponent` (string): 상대방 반응

**응답:**
- `suspicion` (int): 의심도 (0-100)
- `reason` (string): 의심도 판단 이유
- `success` (bool): 성공 여부 (의심도 < 65%)

---

### 4. 변명별 유의사항 생성
**POST** `/generate-cautions`

요청 본문:
```json
{
    "excuses": [
        {
            "text": "변명 내용",
            "reaction": "상대: 반응",
            "grade": "등급",
            "caution": "유의사항"
        },
        ...
    ]
}
```

응답:
```json
{
    "cautions": [
        {
            "excuse": "변명 내용",
            "cautions": [
                "주의사항1",
                "주의사항2",
                "주의사항3"
            ]
        },
        ...
    ]
}
```

**파라미터:**
- `excuses` (array): 변명 목록

---

### 5. 디펜스 반응 조회
**GET** `/sessions/{session_id}/defense-responses`

응답:
```json
{
    "session_id": "session_0",
    "defense_responses": [
        {
            "attempt": 1,
            "response": "상대: 반응1"
        },
        {
            "attempt": 2,
            "response": "상대: 반응2"
        },
        {
            "attempt": 3,
            "response": "상대: 반응3"
        }
    ]
}
```

---

### 6. 헬스 체크
**GET** `/health`

응답:
```json
{
    "status": "ok",
    "server": "AI Server"
}
```

---

## Swagger UI

서버 실행 후: http://localhost:8001/docs

## 외부 접근 설정

### 1. 방화벽 허용 (Windows)
```bash
# PowerShell (관리자 권한)
netsh advfirewall firewall add rule name="Allow AI Server 8001" dir=in action=allow protocol=tcp localport=8001
```

### 2. 자신의 IP 확인
```bash
# PowerShell
ipconfig

# 또는 명령 프롬프트
ipconfig | find "IPv4"
```

### 3. Backend에서 접근
로컬: `http://localhost:8001`
외부: `http://<당신의_IP>:8001`

예시:
- 로컬 IP: `http://192.168.1.100:8001`
- 공인 IP: 필요시 포트포워딩 설정

## 주의사항

- AI 서버는 **독립적**으로 실행되어야 합니다
- `.env` 파일에 `GEMINI_API_KEY`가 설정되어 있어야 합니다
- CORS가 활성화되어 있어 모든 오리진에서 요청 가능합니다
- 외부 공개 시 API 키 보안에 유의하세요
