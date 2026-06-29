from ai.gemini_client import GeminiClient

print("🚀 Gemini API 초기화 중...\n")
client = GeminiClient()
print()

print("=" * 60)
print("디펜스 시뮬레이션 - 인터랙티브")
print("=" * 60)

# 예제 변명과 반응
original_excuse = "몸이 안 좋아서 못 갈 것 같아"
opponent_reaction = "엄마: 또? 증빙 사진 보내줄래?"

conversation_history = []

print(f"\n📍 변명: {original_excuse}")
print(f"🚨 상대 반응: {opponent_reaction}\n")

# 3번 디펜스 시뮬레이션
for attempt in range(1, 4):
    print(f"\n{'=' * 60}")
    print(f"시도 {attempt}/3")
    print(f"{'=' * 60}")

    # 사용자 디펜스 입력
    user_defense = input("\n💬 당신의 디펜스를 입력하세요: ").strip()

    if not user_defense:
        print("⚠️ 입력이 비었습니다.")
        attempt -= 1
        continue

    # 상대 반응 생성
    print("\n🤖 상대 반응 생성 중...\n")
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
print("\n" + "=" * 60)
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
