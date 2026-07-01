import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from ai.gpt_client import GPTClient
from ai.storage import storage

load_dotenv()

# ngrok 설정
try:
    from pyngrok import ngrok
    ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
        print("[OK] ngrok auth token set")
except ImportError:
    print("[WARN] pyngrok not installed. Run: pip install pyngrok")

app = FastAPI(title="AI Server - 변명 생성 (GPT)")

# CORS 설정 - 모든 오리진 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모델 로드
print("[INFO] AI Server initializing...")
ai_client = GPTClient()


# ===== Pydantic Models =====
class GenerateExcuseRequest(BaseModel):
    situation: str
    politeness: int
    credibility: int


class GenerateExcuseResponse(BaseModel):
    excuses: List[Dict[str, Any]]


class DefenseReactionRequest(BaseModel):
    original_excuse: str
    opponent_reaction: str
    user_defense: str
    attempt_num: int


class DefenseReactionResponse(BaseModel):
    reaction: str


class ConversationTurn(BaseModel):
    user: str
    opponent: str


class MeasureSuspicionRequest(BaseModel):
    original_excuse: str
    conversation_history: List[ConversationTurn]


class MeasureSuspicionResponse(BaseModel):
    suspicion: int
    reason: str
    success: bool


# ===== AI Endpoints =====
@app.post("/generate-excuses")
async def generate_excuses(request: GenerateExcuseRequest):
    """
    변명 4개 생성 및 저장
    """
    result = ai_client.generate_excuses(
        situation=request.situation,
        politeness=request.politeness,
        credibility=request.credibility,
    )

    # 결과 저장
    session_id = storage.save_excuse(
        situation=request.situation,
        politeness=request.politeness,
        credibility=request.credibility,
        excuses=result["excuses"],
    )

    return {
        "session_id": session_id,
        "excuses": result["excuses"]
    }


class DefenseReactionRequestWithSession(BaseModel):
    session_id: str
    original_excuse: str
    opponent_reaction: str
    user_defense: str
    attempt_num: int


@app.post("/defense-reaction")
async def generate_defense_reaction(request: DefenseReactionRequestWithSession):
    """
    사용자의 디펜스에 대한 상대 반응 생성 및 저장
    """
    reaction = ai_client.generate_defense_reaction(
        original_excuse=request.original_excuse,
        opponent_reaction=request.opponent_reaction,
        user_defense=request.user_defense,
        attempt_num=request.attempt_num,
    )

    # 대화 턴 저장
    storage.add_defense_turn(
        session_id=request.session_id,
        user_defense=request.user_defense,
        opponent_response=reaction,
    )

    return {"reaction": reaction}


class MeasureSuspicionRequestWithSession(BaseModel):
    session_id: str
    original_excuse: str
    conversation_history: List[ConversationTurn]


@app.post("/measure-suspicion")
async def measure_suspicion(request: MeasureSuspicionRequestWithSession):
    """
    의심도 측정 및 저장
    """
    conversation_history = [
        {"user": turn.user, "opponent": turn.opponent}
        for turn in request.conversation_history
    ]

    result = ai_client.measure_suspicion(
        original_excuse=request.original_excuse,
        conversation_history=conversation_history,
    )

    # 의심도 결과 저장
    storage.save_suspicion_result(
        session_id=request.session_id,
        suspicion=result["suspicion"],
        reason=result["reason"],
        success=result["success"],
    )

    return {
        "suspicion": result["suspicion"],
        "reason": result["reason"],
        "success": result["success"],
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """저장된 세션 조회"""
    session = storage.get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    return session


@app.get("/sessions")
async def get_all_sessions():
    """모든 세션 조회"""
    return storage.get_all_sessions()


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """세션 삭제"""
    success = storage.delete_session(session_id)
    return {"success": success}


class GenerateCautionsRequest(BaseModel):
    excuses: List[Dict[str, Any]]


@app.post("/generate-cautions")
async def generate_cautions(request: GenerateCautionsRequest):
    """
    변명별 유의사항 생성
    """
    result = ai_client.generate_cautions(excuses=request.excuses)
    return result


@app.get("/sessions/{session_id}/defense-responses")
async def get_defense_responses(session_id: str):
    """
    저장된 디펜스 반응 조회
    """
    session = storage.get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    return {
        "session_id": session_id,
        "defense_responses": session.get("defense_responses", [])
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok", "server": "AI Server - 변명 생성 (GPT)"}
