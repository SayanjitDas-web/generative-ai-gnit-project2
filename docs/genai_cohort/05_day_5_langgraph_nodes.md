# Day 5: Intro to Stateful Agents (LangGraph)

## 🎯 Objective
Understand the difference between a "Chat" and an "Agent".

## 🧠 The Theory
A "Chat" is just: `Input -> AI -> Output`.
An "Agent" has **State**. It knows what has happened before and can follow a multi-step plan.

### Introducing LangGraph
LangGraph is a library that helps create AI workflows using **Graphs**.
- **Nodes**: Points of logic (Functions).
- **Edges**: The arrows connecting them.

## 💻 Understanding AgentState
In `ai_engine.py`, we define `AgentState`:
```python
class AgentState(TypedDict):
    messages: List[Dict[str, str]] # Memory of the chat
    session_id: str                # Unique identifier
    topic: str                     # Context
    difficulty: str                # Setting
    next_step: str                 # Flow control
```

## 🧠 Why "State" is King
Without state, the AI wouldn't know if it's currently asking Day 1 questions or Day 10 questions. State provides the **Continuity** needed for a professional interview.

## 🚀 Student Exercise
In `ai_engine.py`, look at `AgentState`. 
If you wanted the AI to track the user's **Current Score** during the chat, what field would you add to this class?
