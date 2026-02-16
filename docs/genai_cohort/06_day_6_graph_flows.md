# Day 6: Building Complex Conversation Flows

## 🎯 Objective
Learn how to compile and execute a LangGraph workflow.

## 🧠 The Theory
Once you have Nodes and State, you need a "Control Room" to manage the flow. This is the **StateGraph**.

### The Compilation Process
1. **Define Graph**: `workflow = StateGraph(AgentState)`
2. **Add Nodes**: `workflow.add_node("interviewer", interview_node)`
3. **Set Entry**: `workflow.set_entry_point("interviewer")`
4. **Compile**: `workflow.compile()`

## 💻 Execution Flow
Look at [sessions.py](file:///c:/Users/user/Desktop/genAI%20projects/project2/backend/routers/sessions.py):
```python
final_state = await interview_graph.ainvoke(inputs, config=config)
```
When we call `ainvoke`, LangGraph:
1. Takes the `inputs`.
2. Passes them through every node in the graph.
3. Returns the **Final state** after the AI has finished its turn.

## 🚀 Student Exercise
Imagine we wanted to add a "Validator Node" to check if the AI's question is too easy.
1. Draw a diagram of how the graph would change.
2. Where would the new edge go? (Interviewer -> Validator -> End)
