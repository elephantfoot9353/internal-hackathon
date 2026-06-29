import os
from dotenv import load_dotenv
from ai.gemini_client import GeminiClient

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = GeminiClient(api_key)

# 변명 생성 테스트
print("=" * 50)
print("변명 생성 테스트")
print("=" * 50)

result = client.generate_excuses(
    situation="약속을 안 가고 싶어",
    politeness=7,  # 존댓말 정중함
    credibility=5,  # 중간 신뢰도
)

print("\n생성된 변명:")
for i, excuse in enumerate(result["excuses"], 1):
    print(f"\n{i}. {excuse['text']}")
    print(f"   상대 반응: {excuse['reaction']}")
    print(f"   등급: {excuse['grade']}")
    print(f"   유의사항: {excuse['caution']}")
