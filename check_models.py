import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GPT_API_KEY")
client = OpenAI(api_key=api_key)

print("사용 가능한 모델들:")
print("=" * 50)
models = client.models.list()
for model in models.data:
    print(f"- {model.id}")
