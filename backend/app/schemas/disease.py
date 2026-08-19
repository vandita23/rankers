from pydantic import BaseModel


class DiseaseResponse(BaseModel):
    disease: str
    confidence: int
    low_confidence: bool
    recommended_actions: list[str]
    language: str
