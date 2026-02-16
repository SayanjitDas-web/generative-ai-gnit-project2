import os
import httpx
from typing import TypedDict, Annotated, List, Union, Dict
from langgraph.graph import StateGraph, END
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    session_id: str
    topic: str
    difficulty: str
    next_step: str

def interview_node(state: AgentState):
    messages = state["messages"]
    topic = state["topic"]
    
    system_prompt = f"""You are an expert AI Interviewer for a {topic} role. 
    Your goal is to conduct a professional and challenging interview.
    Current Difficulty: {state['difficulty']}
    
    Guidelines:
    1. Ask one concise question at a time.
    2. Provide feedback if the user's answer is weak, then move to the next question.
    3. Be encouraging but professional.
    """
    
    api_messages = [{"role": "system", "content": system_prompt}] + messages
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=api_messages,
    )
    
    ai_message = response.choices[0].message.content
    
    return {
        "messages": messages + [{"role": "assistant", "content": ai_message}],
        "next_step": "user_input"
    }

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("interviewer", interview_node)
    workflow.set_entry_point("interviewer")
    workflow.add_edge("interviewer", END)
    return workflow.compile()

interview_graph = build_graph()
