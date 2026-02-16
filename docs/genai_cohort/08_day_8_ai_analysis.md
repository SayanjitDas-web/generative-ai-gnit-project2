# Day 8: AI Feedback & Analysis System

## 🎯 Objective
Use AI to perform deep analysis on a completed session.

## 🧠 The Theory
GenAI is great at **Summarization** and **Evaluation**. 
In Day 7, we learned about JSON. Today, we look at how to gather the *entire* chat history and feed it back to the AI for a final review.

## 💻 Implementation Detail
Look at the `/analyze` endpoint in `sessions.py`.
### 1. The Data Prep
```python
history = "\n".join([f"{m.role}: {m.content}" for m in chat_history])
```
We take all previous messages and turn them into one giant "context block".

### 2. The Analysis Request
We don't just ask "how did it go?". We provide a **Template**:
*"Analyze the following interview transcript and provide a structured feedback JSON."*

## 🧠 Why separate "Interview" from "Analysis"?
1. **Model Choice**: We use `gpt-oss` for the fast chat, but maybe a stronger model (like `Gemini 2.0 Flash`) for the deep analysis.
2. **Context**: The interviewer only sees the "now". The Analyst sees the "whole picture".

## 🚀 Student Exercise
In `sessions.py`, notice we set `session.status = "Completed"`. 
How would you change the prompt to also give the user a **"Pass/Fail"** status based on their score?
