from typing import Dict, List, Optional
from datetime import datetime


class ExcuseStorage:
    """변명 생성 결과를 메모리에 저장하는 저장소"""

    def __init__(self):
        self.excuses: Dict[str, Dict] = {}
        self.counter = 0

    def save_excuse(
        self,
        situation: str,
        politeness: int,
        credibility: int,
        excuses: List[Dict],
    ) -> str:
        """
        변명 저장

        Returns:
            저장된 세션 ID
        """
        session_id = f"session_{self.counter}"
        self.counter += 1

        self.excuses[session_id] = {
            "session_id": session_id,
            "situation": situation,
            "politeness": politeness,
            "credibility": credibility,
            "excuses": excuses,
            "created_at": datetime.now().isoformat(),
            "conversation": [],
            "defense_responses": [],  # 디펜스 반응 저장
            "suspicion_result": None,
        }

        return session_id

    def add_defense_turn(
        self, session_id: str, user_defense: str, opponent_response: str
    ) -> bool:
        """
        디펜스 턴 추가

        Returns:
            성공 여부
        """
        if session_id not in self.excuses:
            return False

        turn = {
            "user": user_defense,
            "opponent": opponent_response,
        }

        self.excuses[session_id]["conversation"].append(turn)
        self.excuses[session_id]["defense_responses"].append({
            "attempt": len(self.excuses[session_id]["defense_responses"]) + 1,
            "response": opponent_response,
        })

        return True

    def save_suspicion_result(
        self, session_id: str, suspicion: int, reason: str, success: bool
    ) -> bool:
        """
        의심도 측정 결과 저장

        Returns:
            성공 여부
        """
        if session_id not in self.excuses:
            return False

        self.excuses[session_id]["suspicion_result"] = {
            "suspicion": suspicion,
            "reason": reason,
            "success": success,
            "completed_at": datetime.now().isoformat(),
        }

        return True

    def get_session(self, session_id: str) -> Optional[Dict]:
        """세션 조회"""
        return self.excuses.get(session_id)

    def get_all_sessions(self) -> Dict[str, Dict]:
        """모든 세션 조회"""
        return self.excuses

    def delete_session(self, session_id: str) -> bool:
        """세션 삭제"""
        if session_id in self.excuses:
            del self.excuses[session_id]
            return True
        return False


# 글로벌 저장소 인스턴스
storage = ExcuseStorage()
