# Day 3: Advanced Personas & System Prompts

## 🎯 Objective
Master "System Prompts" to create high-fidelity AI agents.

## 🧠 The Theory
Every AI conversation has three roles:
1. **System**: The instructions (God Mode).
2. **User**: The human input.
3. **Assistant**: The AI response.

The **System Prompt** is the most powerful. It defines the "Brain" of the AI.

## 💻 Deep Dive: Dynamic Persona
Look at the `interview_node` in `ai_engine.py`:
```python
system_prompt = f"""You are an expert AI Interviewer for a {topic} role. 
Your goal is to conduct a professional and challenging interview.
Current Difficulty: {state['difficulty']}
...
"""
```

### Why use f-strings?
Because it makes our agent **dynamic**. If the user selects "Java Developer", the system prompt *physically changes* before the AI sees it. This is called **Dynamic Templating**.

## 🚀 Student Exercise
Edit the `system_prompt` in `ai_engine.py` to add a specific constraint: *"Speak like a pirate while asking technical questions."* 
Run the app and start a session. See how the persona persists throughout the conversation!
