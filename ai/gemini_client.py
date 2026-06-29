import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Any
from ai.prompt import (
    generate_excuse_prompt,
    generate_defense_reaction_prompt,
    measure_suspicion_prompt,
    generate_caution_prompt,
)

load_dotenv()


class GeminiClient:
    def __init__(self):
        """
        Gemini API 클라이언트 초기화
        """
        api_key = os.getenv("GPT_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_excuses(
        self, situation: str, politeness: int, credibility: int
    ) -> Dict[str, Any]:
        """변명 4개 생성"""
        prompt = generate_excuse_prompt(situation, politeness, credibility)

        response = self.model.generate_content(prompt)
        response_text = response.text

        try:
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"AI 응답을 JSON으로 파싱할 수 없습니다: {e}\n응답: {response_text}")

    def generate_defense_reaction(
        self, original_excuse: str, opponent_reaction: str, user_defense: str, attempt_num: int
    ) -> str:
        """디펜스 반응 생성"""
        prompt = generate_defense_reaction_prompt(
            original_excuse, opponent_reaction, user_defense, attempt_num
        )

        response = self.model.generate_content(prompt)
        response_text = response.text

        try:
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result.get("reaction", "")
        except json.JSONDecodeError:
            return response_text.strip()

    def measure_suspicion(
        self, original_excuse: str, conversation_history: list
    ) -> Dict[str, Any]:
        """의심도 측정"""
        prompt = measure_suspicion_prompt(original_excuse, conversation_history)

        response = self.model.generate_content(prompt)
        response_text = response.text

        try:
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return {
                "suspicion": result.get("suspicion", 100),
                "reason": result.get("reason", ""),
                "success": result.get("suspicion", 100) < 65,
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"의심도 측정 응답을 파싱할 수 없습니다: {e}\n응답: {response_text}")

    def generate_cautions(self, excuses: list) -> Dict[str, Any]:
        """변명별 유의사항 생성"""
        prompt = generate_caution_prompt(excuses)

        response = self.model.generate_content(prompt)
        response_text = response.text

        try:
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text.strip())
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"유의사항 생성 응답을 파싱할 수 없습니다: {e}\n응답: {response_text}")
