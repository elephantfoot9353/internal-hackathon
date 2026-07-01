import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any
from ai.prompt import (
    generate_excuse_prompt,
    generate_defense_reaction_prompt,
    measure_suspicion_prompt,
    generate_caution_prompt,
)

load_dotenv()


class GPTClient:
    def __init__(self):
        """
        OpenAI GPT 클라이언트 초기화
        """
        api_key = os.getenv("GPT_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    def generate_excuses(
        self, situation: str, politeness: int, credibility: int
    ) -> Dict[str, Any]:
        """변명 4개 생성"""
        prompt = generate_excuse_prompt(situation, politeness, credibility)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 창의적인 변명 생성 AI입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 현실적인 상대방 역할을 합니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 심리 분석가입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 실생활 조언 전문가입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content

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
