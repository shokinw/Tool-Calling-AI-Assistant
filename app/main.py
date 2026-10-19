
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import answer_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tool-Calling AI Assistant",
    description="An LLM assistant that executes validated Python tools.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def home():
    return {"message": "Tool-Calling AI Assistant is running!"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = answer_question(request.question)
        return ChatResponse(
            question=request.question,
            answer=answer
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
