# Day 4: SDK & API Integration Architecture

## 🎯 Objective
Learn the professional way to connect a Backend server to an AI Gateway.

## 🧠 The Theory
We don't just send raw strings to a URL. We use an **SDK (Software Development Kit)**. Our project uses the `openai` library because it has become the "industry standard" protocol.

### The Flow:
1. **User** sends message via Browser.
2. **FastAPI** receives it.
3. **SDK Client** authenticates with OpenRouter.
4. **Model** processes and returns a response.

## 💻 Key Project Files
- `.env`: Stores the `OPENROUTER_API_KEY`.
- `ai_engine.py`: Initializes the `client`.
- `requirements.txt`: Lists `openai` as a dependency.

## 🔒 Security Best Practice
**NEVER** put your API keys in the code. 
- Use `.env` file.
- Use `.gitignore` to ensure `.env` is never pushed to GitHub.

## 🚀 Student Exercise
1. Check your `.gitignore` file. Is `.env` included?
2. Try running `print(OPENROUTER_API_KEY)` in `ai_engine.py`. If it shows `None`, your environment variables are not loaded correctly. Fix it using `load_dotenv()`.
