import os
from dotenv import load_dotenv
from ai.gemini_client import GeminiClient

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = GeminiClient(api_key)

print("=" * 60)
print("디펜스 시뮬레이션 테스트")
print("=" * 60)

# 예제 변명과 반응
original_excuse = "몸이 안 좋아서 못 갈 것 같아"
opponent_reaction = "엄마: 또? 증빙 사진 보내줄래?"

conversation_history = []

print(f"\n📍 변명: {original_excuse}")
print(f"🚨 상대 반응: {opponent_reaction}\n")

# 3번 디펜스 시뮬레이션
for attempt in range(1, 4):
    print(f"--- 시도 {attempt}/3 ---")

    # 사용자 디펜스 입력 (실제로는 프론트엔드에서 입력)
    if attempt == 1:
        user_defense = "지금 진짜 열이 나서 침대에 누워있어"
    elif attempt == 2:
        user_defense = "어제부터 감기 기운이 있어서 미리 예방차 쉬고 있는 거야"
    else:
        user_defense = "병원 예약도 했고, 진료비 영수증도 있어"

    print(f"💬 사용자 디펜스: {user_defense}")

    # 상대 반응 생성
    opponent_response = client.generate_defense_reaction(
        original_excuse, opponent_reaction, user_defense, attempt
    )
    print(f"🚨 상대 반응: {opponent_response}\n")

    # 대화 기록 추가
    conversation_history.append({
        "user": user_defense,
        "opponent": opponent_response
    })

# 의심도 측정
print("=" * 60)
print("의심도 측정 중...")
print("=" * 60 + "\n")

result = client.measure_suspicion(original_excuse, conversation_history)

suspicion = result["suspicion"]
reason = result["reason"]
success = result["success"]

print(f"📊 의심도: {suspicion}%")
print(f"📝 판단 이유: {reason}\n")

if success:
    print("✅ 성공! 상대의 의심을 충분히 낮췄습니다!")
else:
    print("❌ 실패! 상대가 여전히 의심하고 있습니다.")
