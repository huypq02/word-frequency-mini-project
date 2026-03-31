from pydantic import BaseModel

class TextStatsRequest(BaseModel):
    text: str
    output_format: str = "json" # json, csv, png

class TextStatsResponse(BaseModel):
    status: str
    message: str
    data: dict
