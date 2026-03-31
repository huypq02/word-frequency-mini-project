import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from typing import Annotated
import time, os
from src.pipeline import text_stats as ts
from src.config.constant import (
    ALLOWED_CONTENT_TYPE_HEADERS,
    ALLOWED_FILE_CONTENT_TYPES,
    APP_IMPORT_PATH,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_PORT,
    OUTPUT_DIR,
    OUTPUT_FILE_PREFIX,
    SUPPORTED_OUTPUT_FORMATS,
    WORDS_COLUMN,
)
from .models import TextStatsRequest, TextStatsResponse
from .middleware import LimitUploadSize, LimitUploadContentType

app = FastAPI()
app.add_middleware(LimitUploadSize)  # Default: 5MB
app.add_middleware(LimitUploadContentType,
                   allowed_file_content_type=ALLOWED_FILE_CONTENT_TYPES,
                   allowed_content_type_header=ALLOWED_CONTENT_TYPE_HEADERS)

@app.post("/analyses/text")
async def analyze_text(request: TextStatsRequest):
    try:
        report_format = request.output_format
        if report_format not in SUPPORTED_OUTPUT_FORMATS:
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

        if WORDS_COLUMN not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure.")
        
        if report_format == "json":
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index(WORDS_COLUMN).to_dict("dict"))
        elif report_format == "csv":
            fname = f"{OUTPUT_FILE_PREFIX}_{time.time_ns()}"
            download_name = f"{fname}.csv"
            ts.export_results(word_stats, download_name, OUTPUT_DIR)
            path_file = os.path.join(OUTPUT_DIR, download_name)
            return FileResponse(path_file, headers={"Content-Disposition": f"attachment; filename={download_name}"})
        elif report_format == "png":
            fname = f"{OUTPUT_FILE_PREFIX}_{time.time_ns()}"
            download_name = f"{fname}.png"
            ts.visualize_results(word_stats, download_name, OUTPUT_DIR)
            path_file = os.path.join(OUTPUT_DIR, download_name)
            return FileResponse(path_file, headers={"Content-Disposition": f"attachment; filename={download_name}"})

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input text: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing text.")

@app.post("/analyses/file")
async def analyze_file(file: Annotated[UploadFile, File(...)],
                       output_format: Annotated[str, Form()] = DEFAULT_OUTPUT_FORMAT):
    try:
        report_format = output_format
        if report_format not in SUPPORTED_OUTPUT_FORMATS:
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

        if WORDS_COLUMN not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure.")

        if report_format == "json":
            return TextStatsResponse(status="success",
                                    message="Text analysis completed successfully.",
                                    data=word_stats.set_index(WORDS_COLUMN).to_dict("dict"))
        elif report_format == "csv":
            fname = f"{OUTPUT_FILE_PREFIX}_{time.time_ns()}"
            download_name = f"{fname}.csv"
            ts.export_results(word_stats, download_name, OUTPUT_DIR)
            path_file = os.path.join(OUTPUT_DIR, download_name)
            return FileResponse(path_file, headers={"Content-Disposition": f"attachment; filename={download_name}"})
        elif report_format == "png":
            fname = f"{OUTPUT_FILE_PREFIX}_{time.time_ns()}"
            download_name = f"{fname}.png"
            ts.visualize_results(word_stats, download_name, OUTPUT_DIR)
            path_file = os.path.join(OUTPUT_DIR, download_name)
            return FileResponse(path_file, headers={"Content-Disposition": f"attachment; filename={download_name}"})

    except UnicodeDecodeError:
        print(f"Failed to decode uploaded file '{file.filename}' as UTF-8 text.")
        raise HTTPException(status_code=400, detail="The uploaded file must be UTF-8 encoded text.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input file: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing file.")

if __name__ == "__main__":
    config = uvicorn.Config(APP_IMPORT_PATH, host=DEFAULT_HOST, port=DEFAULT_PORT, log_level=DEFAULT_LOG_LEVEL)
    server = uvicorn.Server(config)
    server.run()
