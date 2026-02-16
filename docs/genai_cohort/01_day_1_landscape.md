# Day 1: The LLM Landscape & OpenRouter

## 🎯 Objective
Understand the generative AI ecosystem and setup the connectivity foundation.

## 🧠 The Theory
Generative AI models (LLMs) are like high-performance engines. To build a car (App), you need a way to talk to these engines.

### The Providers
- **OpenAI**: GPT-4, GPT-3.5
- **Anthropic**: Claude 3 (Opus, Sonnet, Haiku)
- **Google**: Gemini 1.5, 2.0
- **Meta**: Llama 3 (Open Source)

## 🛠️ The Solution: OpenRouter
Instead of learning 5 different APIs, we use **OpenRouter**. It’s a proxy that gives us access to ALL these models using a single set of keys.

### Why this matters for students:
- **Cost**: No need for expensive individual subscriptions.
- **Speed**: One library to learn.
- **Portability**: Swap models in seconds if one becomes better or cheaper.

## 💻 Code Focus
Check [ai_engine.py](file:///c:/Users/user/Desktop/genAI%20projects/project2/backend/ai_engine.py):
```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)
```

## 🚀 Student Exercise
1. Go to [OpenRouter.ai](https://openrouter.ai/models).
2. Compare the "Prompt Cost" of `gpt-4o` vs `llama-3-70b`. 
3. Discuss why we chose a "free" model for our development phase.
