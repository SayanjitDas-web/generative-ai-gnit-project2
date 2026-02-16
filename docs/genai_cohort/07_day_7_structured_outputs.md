# Day 7: Structured Outputs & JSON Mode

## 🎯 Objective
Force the AI to speak "Code" (JSON) instead of "Language".

## 🧠 The Theory
LLMs are trained to talk like humans. But apps need data. 
If we ask an AI for a "Score", we don't want it to say *"Sure! I'd give them an 80"*. We want `{"score": 80}`.

## 🛠️ The JSON Mode Pattern
In our platform, the Analysis feature uses **JSON Mode**.
### The Prompt Trick:
We include "JSON" in the instructions and provide the **Schema**.
```python
Required JSON keys:
- "strengths": List of strings
- "overall_score": Number
```

## 💻 The API Config
```python
response = client.chat.completions.create(
    model="google/gemini-2.0-flash-001",
    messages=[{"role": "user", "content": analysis_prompt}],
    response_format={"type": "json_object"} # THE MAGIC LINE
)
```

## 🚀 Student Exercise
Open the Analysis tab in the app after an interview.
1. Check the `sessions.py` file. 
2. What happens if the AI forgets a key? (Our app might crash!)
3. Discuss why `json.loads()` is used to turn the string back into a Python object.
