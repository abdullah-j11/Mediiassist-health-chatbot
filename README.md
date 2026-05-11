# 🩺 MediAssist — Health Query Chatbot (FREE VERSION)

Uses **Groq API** (100% free, no credit card) running **LLaMA 3 70B**.

---

## 📁 Project Structure

```
health_chatbot/
├── app.py                  ← Flask backend (safety filter + Groq API)
├── requirements.txt        ← Python packages
├── .env.example            ← Template — rename to .env
├── .env                    ← Your FREE Groq API key (create this)
└── templates/
    └── index.html          ← Chatbot frontend
```

---

## 🚀 Setup (6 Easy Steps)

### Step 1 — Get your FREE Groq API Key
1. Go to **https://console.groq.com/**
2. Click **Sign Up** — no credit card needed!
3. Go to **API Keys** → **Create API Key**
4. Copy the key

### Step 2 — Create your `.env` file
In the `health_chatbot/` folder, create a file named `.env` and add:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3 — Install Python (if not already)
Download from **python.org** (check "Add to PATH" on Windows).

### Step 4 — Install packages
Open terminal in `health_chatbot/` folder:
```bash
pip install -r requirements.txt
```

### Step 5 — Run the server
```bash
python app.py
```

### Step 6 — Open the chatbot
Go to **http://localhost:5000** in your browser 🎉

---

## 🆓 Why Groq is Free
Groq provides free access to open-source models like Meta's LLaMA 3.
Free tier includes generous daily limits — more than enough for this project.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Invalid API key` | Check `.env` file has `GROQ_API_KEY=...` |
| Port 5000 busy | Change `port=5000` to `port=5001` in app.py |
| Page won't load | Make sure `python app.py` is still running |

Stop server: Press **Ctrl + C** in terminal.
