from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from backend.database import get_db
from backend.models import User, InterviewSession, ChatMessage
from backend.schemas import InterviewSessionCreate, InterviewSessionResponse, ChatMessageBase, ChatMessageResponse
from backend.auth import get_current_user
from backend.ai_engine import interview_graph, client
import json

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=InterviewSessionResponse)
async def create_session(session: InterviewSessionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_session = InterviewSession(user_id=current_user.id, topic=session.topic, difficulty=session.difficulty)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

@router.get("/", response_model=List[InterviewSessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(InterviewSession).filter(InterviewSession.user_id == current_user.id))
    return result.scalars().all()

@router.post("/{session_id}/chat", response_model=ChatMessageResponse)
async def chat(session_id: int, message: ChatMessageBase, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify session ownership
    result = await db.execute(select(InterviewSession).filter(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    user_msg = ChatMessage(session_id=session_id, role="user", content=message.content)
    db.add(user_msg)
    await db.flush()
    
    # Get history for LangGraph
    history_result = await db.execute(select(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()))
    history_messages = [{"role": m.role, "content": m.content} for m in history_result.scalars().all()]
    
    # Run AI Engine
    inputs = {
        "messages": history_messages,
        "session_id": str(session_id),
        "topic": session.topic,
        "difficulty": session.difficulty,
        "context": [],
        "next_step": ""
    }
    
    config = {"configurable": {"thread_id": str(session_id)}}
    final_state = await interview_graph.ainvoke(inputs, config=config)
    
    ai_content = final_state["messages"][-1]["content"]
    
    # Save AI response
    ai_msg = ChatMessage(session_id=session_id, role="assistant", content=ai_content)
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)
    
    return ai_msg

@router.get("/{session_id}/history", response_model=List[ChatMessageResponse])
async def get_history(session_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify session ownership
    result = await db.execute(select(InterviewSession).filter(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    result = await db.execute(select(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()))
    return result.scalars().all()

@router.post("/{session_id}/analyze", response_model=InterviewSessionResponse)
async def analyze_session(session_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify session ownership
    result = await db.execute(select(InterviewSession).filter(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Get history
    history_result = await db.execute(select(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()))
    history = "\n".join([f"{m.role}: {m.content}" for m in history_result.scalars().all()])
    
    analysis_prompt = f"""Analyze the following interview transcript and provide a structured feedback JSON.
    Transcript:
    {history}
    
    Required JSON keys:
    - "strengths": List of strings
    - "weaknesses": List of strings
    - "overall_score": Number (0-100)
    - "recommendations": List of strings
    """
    
    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001",
        messages=[{"role": "user", "content": analysis_prompt}],
        response_format={"type": "json_object"}
    )
    
    feedback = json.loads(response.choices[0].message.content)
    
    session.feedback = feedback
    session.status = "Completed"
    await db.commit()
    await db.refresh(session)
    return session
