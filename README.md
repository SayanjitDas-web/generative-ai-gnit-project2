# AI Placement Trainer Platform

A comprehensive AI-powered interview preparation platform built with FastAPI, LangGraph, OpenRouter, and ChromaDB.

## Features
- **User Authentication**: Secure registration and login.
- **AI Interview Sessions**: Topic-specific interviews (Technical, HR, etc.).
- **Long-term Memory**: Uses ChromaDB to remember context across sessions.
- **LangGraph Integration**: Advanced conversational flow management.
- **Performance Analytics**: Detailed feedback on strengths, weaknesses, and scoring.

## Prerequisites
- Python 3.9+
- OpenRouter API Key

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup environment variables:
   - Copy `.env.example` to `.env`.
   - Add your `OPENROUTER_API_KEY` to `.env`.

## Running the Application
1. Start the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
2. Open `frontend/index.html` in your browser.

## Technologies Used
- **Backend**: FastAPI, LangGraph, SQLAlchemy, Pydantic.
- **AI**: OpenRouter (Gemini 2.0 Flash), ChromaDB (Vector Store).
- **Frontend**: Vanilla JS, CSS3 (Glassmorphism), HTML5.
