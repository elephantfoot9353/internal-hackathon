import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GPT_API_KEY")
genai.configure(api_key=api_key)

print("사용 가능한 모델들:")
print("=" * 50)
for model in genai.list_models():
    print(f"- {model.name}")
