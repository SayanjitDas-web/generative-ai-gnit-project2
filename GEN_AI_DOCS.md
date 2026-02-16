# Generative AI Course: Build an AI Placement Trainer
Welcome to the 10-day Generative AI cohort! This documentation breaks down the AI core of our Placement Trainer platform into digestible parts.

## 📅 Day 1-2: The Gateway (OpenRouter & SDK)
In the first phase, we establish a connection to the world's most powerful AI models.

### Why OpenRouter?
Instead of hardcoding for a single provider (like OpenAI or Anthropic), we use **OpenRouter**. It acts as a unified gateway, allowing us to swap models (GPT-4, Claude, Gemini, Llama) with a single line of code.

### Implementation Reference ([ai_engine.py](file:///c:/Users/user/Desktop/genAI%20projects/project2/backend/ai_engine.py))
```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)
```
**Key Concept**: The `OpenAI` client is a standard. By changing the `base_url`, we redirect our requests through OpenRouter's routing layer.

---

## 📅 Day 3-5: The Brain (LangGraph Orchestration)
Simple linear chatbots are easy. Complex, stateful AI agents require **LangGraph**.

### What is LangGraph?
LangGraph allows us to treat AI logic as a **State Machine**. We define "nodes" (functions) and "edges" (paths between them).

### Our Graph Structure
1. **AgentState**: A TypedDict that tracks the interview transcript, topic, and difficulty.
2. **Nodes**: The `interview_node` is our primary logic unit.

```python
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("interviewer", interview_node)
    workflow.set_entry_point("interviewer")
    workflow.add_edge("interviewer", END)
    return workflow.compile()
```
**Key Concept**: Even though our current graph is simple (one node), LangGraph provides the infrastructure to add "HR Nodes", "Technical Nodes", or "Logic Checkers" in the future.

---

## 📅 Day 6-8: The Craft (Prompt Engineering)
The difference between a "chat" and a "professional interview" lies in the **System Prompt**.

### The Interviewer Persona
We inject a persona into the model to control its behavior.
```python
system_prompt = f"""You are an expert AI Interviewer for a {topic} role. 
Your goal is to conduct a professional and challenging interview.
...
Guidelines:
1. Ask one concise question at a time.
2. Provide feedback if the user's answer is weak...
"""
```
### Technical Nuance
We use **f-strings** to dynamically insert the user's chosen `topic` and `difficulty` into the prompt, making हर interview unique.

---

## 📅 Day 9-10: Advanced Patterns (Feedback & JSON)
AI isn't just for talking; it's for **structured analysis**.

### Structured Outputs
In [sessions.py](file:///c:/Users/user/Desktop/genAI%20projects/project2/backend/routers/sessions.py), we use specialized prompts to force the AI to return data in a specific format (JSON).

```python
analysis_prompt = """Analyze the interview... Provide a structured feedback JSON.
Required JSON keys:
- "strengths": List of strings
- "overall_score": Number (0-100)
..."""
```

### Why JSON?
By forcing a `json_object` response format, our Frontend (`app.js`) can easily parse the AI's "thoughts" into beautiful UI components like scorecards and bullet points.

---

## 🎓 Summary for Students
By combining **OpenRouter** (Connectivity), **LangGraph** (Logic), and **Prompt Engineering** (Personality), you have built a system that doesn't just "chat"—it **acts** as a professional coach.
