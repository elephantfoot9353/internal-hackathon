import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

print("[INFO] AI Server starting...")

try:
    from pyngrok import ngrok

    ngrok_token = os.getenv("NGROK_AUTH_TOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
        print("[OK] ngrok auth token set")

        # ngrok 터널 생성
        public_url = ngrok.connect(8001, "http")
        print(f"\n[NGROK] Public URL: {public_url}")
        print(f"[NGROK] Local: http://localhost:8001")
        print(f"[NGROK] External: {public_url}\n")
    else:
        print("[WARN] NGROK_AUTH_TOKEN not found")
except Exception as e:
    print(f"[WARN] ngrok error: {str(e)[:100]}")

print("[INFO] API Docs: http://localhost:8001/docs\n")

uvicorn.run(
    "ai.server:app",
    host="0.0.0.0",
    port=8001,
    reload=True
)
