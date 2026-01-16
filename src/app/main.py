import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from typing import Annotated
import time, os
from src.pipeline import text_stats as ts
from .models import TextStatsRequest, TextStatsResponse
from .middleware import LimitUploadSize, LimitUploadContentType

app = FastAPI()
app.add_middleware(LimitUploadSize)  # Default: 5MB
app.add_middleware(LimitUploadContentType,
                   allowed_file_content_type=['text/plain'],
                   allowed_content_type_header=['multipart/form-data', 'application/json'])

# Ensure NLTK resources are available at startup
ts.ensure_nltk_resources()

@app.post("/analyses/text")
async def analyze_text(request: TextStatsRequest):
    try:
        report_format = request.format
        if report_format not in ['json', 'csv', 'png']:
            raise HTTPException(status_code=415, detail="The format is not supported by the server.")
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
        
        if report_format == 'json':
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index('words').to_dict('dict'))
        elif report_format == 'csv':
            fname = f"word_frequency_{time.time_ns()}"
            download_name = f"{fname}.csv"
            ts.export_results(word_stats, download_name, "output")
            path_file = os.path.join("output", download_name)
            return FileResponse(path_file, headers={'Content-Disposition': f'attachment; filename={download_name}'})
        elif report_format == 'png':
            fname = f"word_frequency_{time.time_ns()}"
            download_name = f"{fname}.png"
            ts.visualize_results(word_stats, download_name, "output")
            path_file = os.path.join("output", download_name)
            return FileResponse(path_file, headers={'Content-Disposition': f'attachment; filename={download_name}'})

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input text: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing text.")

@app.post("/analyses/file")
async def analyze_file(format: Annotated[str, Form()] = 'json', file: UploadFile = File(...)):
    try:
        report_format = format
        if report_format not in ['json', 'csv', 'png']:
            raise HTTPException(status_code=415, detail="The format is not supported by the server.")

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

        if report_format == 'json':
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index('words').to_dict('dict'))
        elif report_format == 'csv':
            fname = f"word_frequency_{time.time_ns()}"
            download_name = f"{fname}.csv"
            ts.export_results(word_stats, download_name, "output")
            path_file = os.path.join("output", download_name)
            return FileResponse(path_file, headers={'Content-Disposition': f'attachment; filename={download_name}'})
        elif report_format == 'png':
            fname = f"word_frequency_{time.time_ns()}"
            download_name = f"{fname}.png"
            ts.visualize_results(word_stats, download_name, "output")
            path_file = os.path.join("output", download_name)
            return FileResponse(path_file, headers={'Content-Disposition': f'attachment; filename={download_name}'})

    except UnicodeDecodeError:
        print(f"Failed to decode uploaded file '{file.filename}' as UTF-8 text.")
        raise HTTPException(status_code=400, detail="The uploaded file must be UTF-8 encoded text.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input file: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing file.")

if __name__ == "__main__":
    config = uvicorn.Config("src.app.main:app", host="0.0.0.0", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
