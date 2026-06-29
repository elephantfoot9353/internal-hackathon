import httpx
import json

# ngrok URL 또는 로컬 서버
BASE_URL = "https://knee-tribunal-angular.ngrok-free.dev"
# BASE_URL = "http://localhost:8001"  # 로컬 테스트

print(f"🚀 AI 서버 연결 중: {BASE_URL}\n")
client = httpx.Client(base_url=BASE_URL, timeout=30.0)

print("=" * 60)
print("변명 생성 - 전체 플로우")
print("=" * 60)

# 1단계: 상황 선택
print("\n【 1단계: 상황 선택 】")
print("-" * 60)

situations = {
    "1": "약속",
    "2": "과제·팀플",
    "3": "회식·모임",
    "4": "알바",
    "5": "가족 행사"
}

print("\n상황을 선택하세요:")
for key, value in situations.items():
    print(f"{key}. {value}")

choice = input("\n선택 (1-5): ").strip()
base_situation = situations.get(choice, "약속")

detail = input(f"\n{base_situation}에 대해 자세하게 입력하세요 (예: 친구와의 저녁 약속): ").strip()
situation = f"{base_situation} - {detail}" if detail else base_situation

politeness = int(input("\n🎤 정중함을 선택하세요 (1=막말, 5=보통, 10=존댓말): ").strip())
credibility = int(input("🎯 신뢰도를 선택하세요 (1=거짓, 5=보통, 10=진짜): ").strip())

print("\n🤖 변명 생성 중...\n")
response = client.post("/generate-excuses", json={
    "situation": situation,
    "politeness": politeness,
    "credibility": credibility,
})
result = response.json()

print("생성된 변명:")
for i, excuse in enumerate(result["excuses"], 1):
    print(f"\n{i}. {excuse['text']}")
    print(f"   반응: {excuse['reaction']}")
    print(f"   등급: {excuse['grade']}")
    print(f"   주의: {excuse['caution']}")

# 2단계: 변명 선택
print("\n" + "=" * 60)
print("【 2단계: 변명 선택 】")
print("-" * 60)

choice = int(input("\n선택할 변명 번호를 입력하세요 (1-4): ").strip())
selected_excuse = result["excuses"][choice - 1]

print(f"\n✅ 선택한 변명: {selected_excuse['text']}")

# 3단계: 디펜스 시뮬레이션
print("\n" + "=" * 60)
print("【 3단계: 디펜스 시뮬레이션 】")
print("=" * 60)

original_excuse = selected_excuse["text"]
opponent_reaction = selected_excuse["reaction"]

conversation_history = []

print(f"\n📍 변명: {original_excuse}")
print(f"🚨 상대 반응: {opponent_reaction}\n")

# 3번 디펜스
for attempt in range(1, 4):
    print(f"\n{'=' * 60}")
    print(f"시도 {attempt}/3")
    print(f"{'=' * 60}")

    user_defense = input("\n💬 당신의 디펜스를 입력하세요: ").strip()

    if not user_defense:
        print("⚠️ 입력이 비었습니다.")
        attempt -= 1
        continue

    print("\n🤖 상대 반응 생성 중...\n")
    response = client.post("/defense-reaction", json={
        "session_id": "test_session",
        "original_excuse": original_excuse,
        "opponent_reaction": opponent_reaction,
        "user_defense": user_defense,
        "attempt_num": attempt,
    })
    opponent_response = response.json()["reaction"]
    print(f"🚨 상대 반응: {opponent_response}\n")

    conversation_history.append({
        "user": user_defense,
        "opponent": opponent_response
    })

# 4단계: 의심도 측정
print("\n" + "=" * 60)
print("【 4단계: 의심도 측정 】")
print("=" * 60 + "\n")

print("🤖 의심도 측정 중...\n")
response = client.post("/measure-suspicion", json={
    "session_id": "test_session",
    "original_excuse": original_excuse,
    "conversation_history": conversation_history,
})
result = response.json()

suspicion = result["suspicion"]
reason = result["reason"]
success = result["success"]

print(f"📊 의심도: {suspicion}%")
print(f"📝 판단 이유: {reason}\n")

if success:
    print("✅ 성공! 상대의 의심을 충분히 낮췄습니다!")
else:
    print("❌ 실패! 상대가 여전히 의심하고 있습니다.")
