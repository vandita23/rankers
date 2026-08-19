from pydantic import BaseModel, Field


class SchemeQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    language: str = Field(default="en", pattern="^(en|hi)$")


class SchemeResult(BaseModel):
    name: str
    summary: str
    eligibility: list[str]
    documents: list[str]
    steps: list[str]
    source: str


class SchemeQueryResponse(BaseModel):
    answer: str
    schemes: list[SchemeResult]
    language: str
