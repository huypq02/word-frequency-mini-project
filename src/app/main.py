from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import Annotated
from fastapi.responses import StreamingResponse
from pipeline import text_stats as ts
from .models import TextStatsRequest, TextStatsResponse
from .middleware import LimitUploadSize, LimitUploadContentType
import time, os

app = FastAPI()
app.add_middleware(LimitUploadSize)  # Default: 5MB
# app.add_middleware(LimitUploadContentType,
#                    allowed_file_content_type=['text/plain'],
#                    allowed_content_type_header=['multipart/form-data', 'application/json'])

@app.post("/analyses/text")
async def analyze_text(request: TextStatsRequest):
    try:
        # Validate input text
        if request.text is None or request.text.strip() == "":
            raise HTTPException(status_code=400, detail="Input text must not be empty or whitespace-only.")

        # Preprocessing data
        token = ts.preprocessing(request.text)
        # Get word statistics
        word_stats = ts.statistics(token)

        # Validate Dataframe structure
        if word_stats.empty:
            raise HTTPException(status_code=500, detail="No words found after processing data.")

        if 'words' not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure.")
        
        if request.format == 'json':
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index('words').to_dict('dict'))
        elif request.format == 'csv':
            fname = f"word_frequency_{time.time_ns()}.csv"
            ts.export_results(word_stats, fname, "output")
            path_file = os.path.join("output", fname)
            def iterfile():
                with open(path_file, mode="rb") as file_like:
                    yield from file_like
            return StreamingResponse(iterfile(), media_type="text/csv")
        elif request.format == 'png':
            fname = f"word_frequency_{time.time_ns()}.png"
            ts.visualize_results(word_stats, fname, "output")
            path_file = os.path.join("output", fname)
            def iterfile():
                with open(path_file, mode="rb") as file_like:
                    yield from file_like
            return StreamingResponse(iterfile(), media_type="image/png")
        else:
            raise HTTPException(status_code=415, detail="The format is not supported by the server.")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input text: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing text.")

@app.post("/analyses/file")
async def analyze_file(format: Annotated[str, Form()] = 'json', file: UploadFile = File(...)):
    try:
        data = await file.read()
        text = data.decode("utf-8")
        # Validate input text
        if text.strip() == "":
            raise HTTPException(status_code=400, detail="Input text must not be empty or whitespace-only.")

        # Preprocessing data
        token = ts.preprocessing(text)
        # Get word statistics
        word_stats = ts.statistics(token)

        # Validate Dataframe structure
        if word_stats.empty:
            raise HTTPException(status_code=500, detail="No words found after processing data.")

        if 'words' not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure.")

        if format == 'json':
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index('words').to_dict('dict'))
        elif format == 'csv':
            fname = f"word_frequency_{time.time_ns()}.csv"
            ts.export_results(word_stats, fname, "output")
            path_file = os.path.join("output", fname)
            def iterfile():
                with open(path_file, mode="rb") as file_like:
                    yield from file_like
            return StreamingResponse(iterfile(), media_type="text/csv")
        elif format == 'png':
            fname = f"word_frequency_{time.time_ns()}.png"
            ts.visualize_results(word_stats, fname, "output")
            path_file = os.path.join("output", fname)
            def iterfile():
                with open(path_file, mode="rb") as file_like:
                    yield from file_like
            return StreamingResponse(iterfile(), media_type="image/png")
        else:
            raise HTTPException(status_code=415, detail="The format is not supported by the server.")

    except UnicodeDecodeError:
        print(f"Failed to decode uploaded file '{file.filename}' as UTF-8 text.")
        raise HTTPException(status_code=400, detail="The uploaded file must be UTF-8 encoded text.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input file: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing file.")
