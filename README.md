🩺 MediAssist — Health Query Chatbot
MediAssist is a full-stack AI health information assistant that answers general health questions in plain language, while enforcing strict safety boundaries around diagnosis, medication, and emergencies. It's built with a Flask backend, a Groq-hosted LLaMA 3.3 70B model, and a custom two-layer safety filtering system designed to keep responses informative without crossing into medical advice.

✨ Features
Conversational health Q&A — clear, jargon-free answers to general symptom, medication, and wellness questions
Two-layer safety system

Layer 1 — Regex safety filter: intercepts high-risk queries (self-harm, illegal/controlled substances) before they ever reach the model and returns a safe, pre-written response
Layer 2 — System-prompt guardrails: instructs the model to never diagnose, never give dosages, always defer to a doctor for serious symptoms, and to immediately surface emergency numbers when relevant

Emergency-aware — automatically flags emergency contact numbers (115 PK / 911 US / 999 UK) for urgent symptoms or mental health crises
Multi-turn context — maintains conversation history so follow-up questions stay coherent
Clean, responsive chat UI — typing indicators, example prompt chips, and a persistent safety disclaimer banner
Free to run — powered by Groq's free tier (LLaMA 3.3 70B), no paid API required


🛠️ Tech Stack
LayerTechnologyBackendPython, Flask, Flask-CORSAI ModelLLaMA 3.3 70B via Groq APISafety FilteringCustom regex-based pre-filter + prompt-engineered guardrailsFrontendHTML, CSS, vanilla JavaScriptConfigpython-dotenv

📁 Project Structure
Mediiassist-health-chatbot/
├── app.py                
├── templates/
│   └── index.html       
├── requirements.txt      
├── .env.example          
└── .gitignore

How the Safety System Works
Pre-filter (Layer 1): every incoming message is checked against regex patterns covering self-harm and illegal substance requests. Matches are blocked instantly with a safe canned response — the request never reaches the LLM.
Prompt-engineered guardrails (Layer 2): for everything else, the system prompt constrains the model to avoid diagnosis, dosages, and medication-stoppage advice, and to redirect emergencies to local emergency numbers.



