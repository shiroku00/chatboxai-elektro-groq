from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Client Groq (API key dari environment)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
Kamu adalah seorang teknisi elektro ahli.
Spesialis di bidang:
- Instalasi listrik
- Elektronika analog & digital
- Motor listrik
- Panel kontrol & PLC
- Troubleshooting kelistrikan industri

ATURAN PENTING:
- Hanya jawab pertanyaan yang berhubungan dengan elektro, kelistrikan, atau elektronika.
- Jika pertanyaan TIDAK berhubungan dengan bidang elektro, jawab dengan:
  "Maaf, pertanyaan tersebut tidak berkaitan dengan bidang elektro."

Gunakan bahasa Indonesia yang jelas, teknis, dan profesional.
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",  
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render pakai PORT
    app.run(host="0.0.0.0", port=port)
