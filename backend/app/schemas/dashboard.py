from pydantic import BaseModel


class Farmer(BaseModel):
    name: str
    location: str
    crops: list[str]


class Alert(BaseModel):
    id: str
    level: str
    text: str


class ActionItem(BaseModel):
    id: str
    done: bool
    text: str


class DashboardResponse(BaseModel):
    farmer: Farmer
    alerts: list[Alert]
    action_plan: list[ActionItem]
    language: str
