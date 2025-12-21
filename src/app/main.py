from fastapi import FastAPI
from pipeline import text_stats as ts
from .models import TextStatsRequest, TextStatsResponse

app = FastAPI()

@app.post("/analyze-text")
async def analyze_text(request: TextStatsRequest):
     # Preprocessing data
    token = ts.preprocessing(request.text)
    # Get word statistics
    word_stats = ts.statistics(token)

    return TextStatsResponse(status="success",
                             message="Text analysis completed successfully",
                             data=word_stats.set_index('words').to_dict('dict'))