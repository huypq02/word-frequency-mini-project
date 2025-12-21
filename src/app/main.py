from fastapi import FastAPI, UploadFile, File
from pipeline import text_stats as ts
from .models import TextStatsRequest, TextStatsResponse, FileStatsResponse

app = FastAPI()

@app.post("/analyze-text")
async def analyze_text(request: TextStatsRequest):
     # Preprocessing data
    token = ts.preprocessing(text=request.text)
    # Get word statistics
    word_stats = ts.statistics(token)

    return TextStatsResponse(status="success",
                             message="Text analysis completed successfully",
                             data=word_stats.set_index('words').to_dict('dict'))

@app.post("/analyze-file")
async def analyze_text(file: UploadFile = File(...)):
    data = await file.read()
    file.close() # Close file
    text = data.decode("utf-8") # Convert bytes to string

    # Preprocessing data
    token = ts.preprocessing(text=text)
    # Get word statistics
    word_stats = ts.statistics(token)

    return FileStatsResponse(status="success",
                             message="Text analysis completed successfully",
                             filename=file.filename,
                             data=word_stats.set_index('words').to_dict('dict'))