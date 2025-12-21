from pydantic import BaseModel
import pandas as pd
from io import TextIOWrapper

class TextStatsRequest(BaseModel):
    text: str

class TextStatsResponse(BaseModel):
    status: str
    message: str
    data: dict

class FileStatsResponse(BaseModel):
    status: str
    message: str
    filename: str
    data: dict