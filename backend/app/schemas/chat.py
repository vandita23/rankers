from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en", pattern="^(en|hi)$")


class ChatResponse(BaseModel):
    reply: str
    sources: list[str] = []
    language: str
