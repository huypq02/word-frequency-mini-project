from pydantic import BaseModel
import pandas as pd

class TextStatsRequest(BaseModel):
    text: str

class TextStatsResponse(BaseModel):
    status: str
    message: str
    data: dict