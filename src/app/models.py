from pydantic import BaseModel

class TextStatsRequest(BaseModel):
    text: str
    format: str = "json" # json, csv, png

class TextStatsResponse(BaseModel):
    status: str
    message: str
    data: dict
