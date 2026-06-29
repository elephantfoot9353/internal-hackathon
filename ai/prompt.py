def generate_excuse_prompt(situation: str, politeness: int, credibility: int) -> str:
    """
    변명 생성 프롬프팅

    Args:
        situation: 상황 (예: "약속", "과제", "회식")
        politeness: 정중함 (1-10, 1=막말, 10=존댓말)
        credibility: 신뢰도 (1-10, 1=누가 봐도 뻥, 10=안 들킴)

    Returns:
        프롬프팅 문자열
    """

    if politeness >= 9:
        tone_politeness = "존댓말로 매우 정중하게"
    elif politeness >= 7:
        tone_politeness = "존댓말로 정중하게"
    elif politeness >= 5:
        tone_politeness = "존댓말로 보통"
    elif politeness >= 3:
        tone_politeness = "반말로 보통"
    else:
        tone_politeness = "반말로 매우 편하게"
    tone_credibility = "그럴듯하고 믿음직스럽게" if credibility >= 7 else "중간 정도로" if credibility >= 4 else "명백히 거짓 같지만 유머러스하게"

    prompt = f"""당신은 창의적인 변명 생성 AI입니다.

주어진 상황에 대해 그럴듯한 변명을 생성하세요.

【 상황 】
{situation}

【 톤 조절 】
정중함: {politeness}/10 ({tone_politeness})
신뢰도: {credibility}/10 ({tone_credibility})

【 요청 】
위의 상황과 톤에 맞게 다음을 JSON 형식으로 생성해주세요:

1. 변명 4개
2. 각 변명마다:
   - 예상되는 상대 반응 (상대의 입장에서 의심하거나 질문하는 형태로 "상대: 반응내용" 형식으로)
     * 상대는 변명을 완전히 믿지 말고 의심하거나 추가 설명을 요청해야 합니다
     * 예: "정말? 어디가 안 좋아?", "증명할 수 있어?", "왜 미리 말 안 했어?"
   - 변명 등급 (S, A, B, C, D, F 중 하나)
     - S: 아무도 못 캐냄
     - A: 거의 들키지 않음
     - B: 어느 정도 설득력 있음
     - C: 반반 정도
     - D: 의심스러움
     - F: 친구가 너 거기 있는 거 봤음
   - 유의사항 (이 변명을 사용할 때 주의할 점)

【 응답 형식 】
{{
    "excuses": [
        {{
            "text": "변명 내용",
            "reaction": "상대: 반응",
            "grade": "등급",
            "caution": "유의사항"
        }},
        ...
    ]
}}

JSON만 반환하세요. 설명이나 다른 텍스트는 포함하지 마세요."""

    return prompt


def generate_defense_reaction_prompt(
    original_excuse: str, opponent_reaction: str, user_defense: str, attempt_num: int
) -> str:
    """
    사용자의 디펜스 말에 대한 상대의 반응 생성

    Args:
        original_excuse: 원래 변명
        opponent_reaction: 상대의 초기 반응
        user_defense: 사용자의 디펜스 말
        attempt_num: 시도 횟수 (1-3)

    Returns:
        프롬프팅 문자열
    """
    if attempt_num == 1:
        context = "첫 번째 설명입니다. 사용자의 답변이 구체적이고 그럴듯하면 일부 설득될 여지가 있습니다."
    elif attempt_num == 2:
        context = "두 번째 설명입니다. 사용자가 추가 정보나 증거를 제시했다면 더 쉽게 설득될 수 있습니다."
    else:
        context = "세 번째(마지막) 설명입니다. 누적된 설득 시도가 있으므로 사용자의 말이 좋으면 완전히 설득될 가능성도 있습니다."

    prompt = f"""당신은 현실적인 상대방 역할을 하고 있습니다.

【 상황 】
당신은 상대방입니다. 사용자가 처음에 이렇게 변명했습니다:
"{original_excuse}"

【 당신의 초기 반응 】
"{opponent_reaction}"

【 사용자의 새로운 답변 】
"{user_defense}"

【 맥락 】
{context}

【 요청 】
사용자의 답변을 듣고 자연스러운 반응을 생성하세요.
- 사용자의 답변의 구체성과 신뢰성을 고려하세요
- 좋은 답변이면 점진적으로 설득되세요
- 부족한 답변이면 의심하거나 질문해주세요
- 상대가 쉽게 받아들이지 말고, 항상 의심의 여지를 남기세요
- 더 자세한 설명을 요구하거나, 확인 질문을 하세요
- 완전히 설득되기 전까지는 약간의 의심을 유지하세요
- 상대의 입장에서 자연스럽고 현실적인 반응을 하세요

JSON 형식: {{"reaction": "상대방의 반응"}}"""

    return prompt


def measure_suspicion_prompt(
    original_excuse: str, conversation_history: list
) -> str:
    """
    전체 대화를 보고 의심도 측정

    Args:
        original_excuse: 원래 변명
        conversation_history: 대화 기록 (각 항목: {"user": "...", "opponent": "..."})

    Returns:
        프롬프팅 문자열
    """
    conversation_text = "\n".join(
        [
            f"사용자: {turn['user']}\n상대: {turn['opponent']}"
            for turn in conversation_history
        ]
    )

    prompt = f"""당신은 심리 분석가입니다. 주어진 대화를 분석하여 상대방의 의심도를 측정하세요.

【 원래 변명 】
"{original_excuse}"

【 대화 기록 】
{conversation_text}

【 평가 기준 】
다음 요소들을 종합적으로 고려하여 의심도를 판단하세요:

1. 사용자의 답변 품질
   - 구체적이고 상세한가?
   - 신뢰할 수 있는가?
   - 일관성이 있는가?

2. 상대방의 반응
   - 점진적으로 설득되고 있는가?
   - 여전히 의심하고 있는가?
   - 질문이나 요구가 있는가?

3. 누적 효과
   - 여러 번의 설득 시도를 고려하세요
   - 초기에는 의심도가 높을 수 있습니다
   - 좋은 답변이 누적되면 의심도가 낮아집니다

【 의심도 해석 】
- 0%: 완전히 믿음
- 25~40%: 대부분 믿음
- 40~60%: 반반 정도 의심
- 60~80%: 상당히 의심
- 100%: 완벽히 의심함

【 요청 】
위 기준을 바탕으로 현재 상대방의 의심도를 판단하세요.

JSON 형식: {{"suspicion": 숫자(0-100), "reason": "의심도 판단 이유"}}"""

    return prompt


def generate_caution_prompt(excuses: list) -> str:
    """
    변명별 유의사항 생성

    Args:
        excuses: 변명 목록 (각 항목: {"text": "변명 내용", ...})

    Returns:
        프롬프팅 문자열
    """
    excuses_text = "\n".join(
        [f"{i+1}. {excuse['text']}" for i, excuse in enumerate(excuses)]
    )

    prompt = f"""당신은 실생활 조언 전문가입니다.

【 변명 목록 】
{excuses_text}

【 요청 】
각 변명을 실행할 때 들킬 수 있는 상황을 피하기 위한 구체적인 행동 유의사항을 생성하세요.

각 변명마다:
- 피해야 할 행동들
- 일관성 유지 방법
- SNS/통신 주의사항
- 추가 증거 준비 필요시 언급

예시:
변명: "몸이 안 좋아서 집에 있어"
유의사항: "인스타그램 스토리에 활동 내용 올리지 말기, 친구 전화는 조용한 환경에서 받기, 병원 영수증 준비"

【 응답 형식 】
{{
    "cautions": [
        {{
            "excuse": "변명 내용",
            "cautions": ["주의사항1", "주의사항2", "주의사항3"]
        }},
        ...
    ]
}}

JSON만 반환하세요."""

    return prompt
