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
        tone_politeness = "존댓말로 매우 정중하게. 정중한 사과와 배려 (예: 죄송합니다, 그러하겠습니다, 폐를 끼쳐드려 죄송합니다)"
    elif politeness >= 7:
        tone_politeness = "존댓말로 정중하게. 진심 어린 사과 (예: 죄송해요, 그렇게 하겠어요, 정말 죄송합니다)"
    elif politeness >= 5:
        tone_politeness = "존댓말로 보통. 기본적인 사과 (예: 미안해요, 죄송한데요, 그럼 다음에)"
    elif politeness >= 3:
        tone_politeness = "반말로 보통. 짧은 사과 (예: 미안해, 이번엔 못 가, 다음에 봐)"
    elif politeness >= 2:
        tone_politeness = "반말로 편함. 사과가 짧고 대충 (예: 미안, 뭐 어때, 다음에 봐, 그냥 못 가)"
    else:
        tone_politeness = "반말로 거칠게. 사과도 없고 당당하게 (예: 아 몰라, 나 못 가, 알아서 해, 그냥 싫어)"

    if credibility >= 9:
        tone_credibility = "누구도 의심할 수 없는 완벽한 변명. 등급은 S 위주로 생성"
    elif credibility >= 7:
        tone_credibility = "자세히 보지 않으면 진짜인지 모를 수준. 등급은 A, B 위주로 생성"
    elif credibility >= 4:
        tone_credibility = "평범한 변명. 약간 의심스러움. 등급은 B, C, D 위주로 생성"
    elif credibility >= 2:
        tone_credibility = "거짓말인 게 느껴지지만 그나마 그럴듯함. 등급은 D, F 위주로 생성"
    else:
        tone_credibility = "누가 들어도 황당한 거짓말. 등급은 F 위주로 생성"

    prompt = f"""당신은 창의적인 변명 생성 AI입니다.

주어진 상황에 대해 그럴듯한 변명을 생성하세요.

【 상황 】
{situation}

【 톤 조절 】
정중함: {politeness}/10 ({tone_politeness})
신뢰도: {credibility}/10 ({tone_credibility})

【 중요한 지시사항 】
- 변명은 자연스럽고 일상적인 문장이어야 함 (어색하거나 부자연스러운 표현 금지)
- 정중함 레벨에 따라 사과의 방식이 달라져야 함:
  * 정중함 9~10: "정중하고 진심 어린 사과" (죄송합니다, 죄송해요)
  * 정중함 7~8: "기본적인 사과" (죄송해요, 미안해요)
  * 정중함 5~6: "간단한 사과" (미안해요)
  * 정중함 3~4: "짧은 사과" (미안해, 오늘은 못 가)
  * 정중함 2: "최소한의 사과" (뭐 어때, 다음에)
  * 정중함 1: "이유만 진술, 사과 없음, 극도로 단호한 톤" (예: "나 집에 있어야 해. 못 나가" - "그래서" 같은 연결사 사용 금지, 당당하게 끝내기)

【 요청 】
위의 상황과 톤에 맞게 다음을 JSON 형식으로 생성해주세요:

1. 변명 4개 (자연스럽고 일상적인 문장으로)
2. 각 변명마다:
   - 예상되는 상대 반응 (상대의 입장에서 의심하거나 질문하는 형태로 "상대: 반응내용" 형식으로)
     * 상대는 변명을 완전히 믿지 말고 의심하거나 추가 설명을 요청해야 합니다
     * 반응은 변명의 구체적인 내용에 기반해야 하며, 이미 제시된 정보를 무시하고 다시 같은 질문하지 말 것
     * 톤도 사용자의 정중함 레벨({politeness}/10)과 일치해야 함
     * 예: "정말? 어디가 안 좋아?", "증명할 수 있어?", "왜 미리 말 안 했어?"
   - 변명 등급 (S, A, B, C, D, F 중 하나) - 신뢰도 {credibility}에 맞게 선택할 것
     - S: 완벽한 변명, 누구도 의심할 수 없음 (신뢰도 9~10)
     - A: 거의 들키지 않음 (신뢰도 7~8)
     - B: 어느 정도 설득력 있음 (신뢰도 4~6)
     - C: 반반 정도 (신뢰도 3~5)
     - D: 거짓말 같지만 그나마 그럴듯함 (신뢰도 1~3)
     - F: 누가 봐도 황당한 거짓말 (신뢰도 1)
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

0. 원래 변명 자체의 현실성 (가장 중요!)
   - 변명이 현실적이고 가능한가? (예: 친구 약속, 몸 안 좋음) → 대화에 따라 의심도 조정
   - 아니면 비현실적이고 황당한가? (예: 요정, 마법, 피카소 그림, 우주적 현상) → 의심도는 거의 100%에 고정
   - 비현실적인 변명의 의심도는 절대 80% 이하로 내려가면 안 됨. 95~100% 범위 유지

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
   - 현실적인 변명: 의심도가 점진적으로 낮아질 수 있음
   - 비현실적인 변명: 아무리 설득해도 의심도는 95~100% 범위에서만 유지 (절대 80% 이하로 내려가면 안 됨)

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
