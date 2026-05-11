"""
MediAssist Health Chatbot
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import os, re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── Groq Client (FREE) ────────────────────────────────────────────────────────
# Uses LLaMA 3 70B — powerful open-source model, completely free on Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── SYSTEM PROMPT (Prompt Engineering) ───────────────────────────────────────
SYSTEM_PROMPT = """You are MediAssist, a friendly and knowledgeable general health information assistant. Your role is to provide clear, accurate, and helpful information about health topics in plain language.

CORE BEHAVIOR:
- Be warm, empathetic, and easy to understand. Avoid jargon; explain medical terms when you use them.
- Provide evidence-based general health information.
- When relevant, mention both general information AND when to see a doctor.

SAFETY RULES (ALWAYS FOLLOW THESE):
1. NEVER diagnose a specific condition. Say "this could be..." not "you have...".
2. ALWAYS remind users to consult a healthcare professional for serious symptoms.
3. For emergencies (chest pain, difficulty breathing, stroke signs), IMMEDIATELY say to call emergency services: 115 (Pakistan), 911 (USA), 999 (UK).
4. For mental health crises, IMMEDIATELY direct to emergency services or a helpline.
5. NEVER give specific dosage instructions. Say "follow package instructions or ask your pharmacist."
6. NEVER advise stopping prescribed medication. Say "speak to your doctor first."
7. Decline questions about obtaining controlled/illegal substances.

RESPONSE FORMAT:
- Keep answers concise: 3-5 sentences for simple questions, slightly more for complex ones.
- Always end with a brief reminder to consult a doctor when appropriate.
- Use a warm, helpful tone — like a knowledgeable friend, not a textbook."""

# ── Layer 1: Safety Filter (runs before API call) ─────────────────────────────
BLOCKED_PATTERNS = [
    {
        "pattern": re.compile(
            r"how to (overdose|kill|harm|poison|hurt) (myself|yourself|someone)",
            re.IGNORECASE,
        ),
        "response": "I can't provide that information. If you or someone is in crisis, please call 115 (Pakistan) or your local emergency number immediately.",
    },
    {
        "pattern": re.compile(
            r"how (do i|can i|to) (get|buy|obtain) (prescription|controlled|illegal)",
            re.IGNORECASE,
        ),
        "response": "I'm unable to help with that. Please speak with a licensed doctor or pharmacist for any medication needs.",
    },
    {
        "pattern": re.compile(
            r"(recipe|how to make).*(drug|meth|cocaine|heroin|fentanyl)", re.IGNORECASE
        ),
        "response": "I can't assist with that. If you're struggling with substance use, please reach out to a healthcare professional.",
    },
]


def check_safety_filter(text: str):
    for rule in BLOCKED_PATTERNS:
        if rule["pattern"].search(text):
            return rule["response"]
    return None


# ── Routes ────────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        # Get latest user message for safety check
        latest_user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )

        # Layer 1: Safety filter
        blocked = check_safety_filter(latest_user_msg)
        if blocked:
            return jsonify({"response": blocked, "safety_filtered": True})

        # Layer 2: Call Groq API (FREE — LLaMA 3 model)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, powerful open-source model
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
            max_tokens=1024,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        err = str(e)
        if "api_key" in err.lower() or "authentication" in err.lower():
            return jsonify({"error": "Invalid API key. Check your .env file."}), 401
        if "rate" in err.lower():
            return jsonify({"error": "Rate limit reached. Please wait a moment."}), 429
        return jsonify({"error": f"Error: {err}"}), 500


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "running",
            "model": "llama3-70b-8192 via Groq (FREE)",
            "api_key_set": bool(os.getenv("GROQ_API_KEY")),
        }
    )


if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n⚠️  GROQ_API_KEY not found in .env file!")
        print("   1. Go to: https://console.groq.com/")
        print("   2. Sign up FREE — no credit card needed")
        print("   3. Go to API Keys → Create Key")
        print("   4. Paste it into your .env file as: GROQ_API_KEY=your_key\n")
    else:
        print(f"\n✅  Groq API key loaded ({api_key[:12]}...)")
    print("🚀  Starting MediAssist (FREE — powered by LLaMA 3 via Groq)...")
    print("🌐  Open browser at: http://localhost:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
