from pydantic import BaseModel, Field
from fastapi import FastAPI

from ai_agent.agent.graph import run_agent
from ai_agent.config import settings

app = FastAPI(title="AI Agent RAG API", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=8000)


class AskResponse(BaseModel):
    answer: str
    model: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-agent-rag"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    answer = run_agent(request.question)
    return AskResponse(answer=answer, model=settings.openai_model)
