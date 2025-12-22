from pydantic import BaseModel

class TextStatsRequest(BaseModel):
    text: str

class TextStatsResponse(BaseModel):
    status: str
    message: str
    data: dict
