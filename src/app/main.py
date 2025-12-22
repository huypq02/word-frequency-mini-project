from fastapi import FastAPI, UploadFile, File, HTTPException
from pipeline import text_stats as ts
from .models import TextStatsRequest, TextStatsResponse

app = FastAPI()

@app.post("/analyze-text")
async def analyze_text(request: TextStatsRequest):
    try:
        # Validate input text
        if request.text is None or request.text.strip() == "":
            raise HTTPException(status_code=400, detail="Input text must not be empty or whitespace-only")

        # Preprocessing data
        token = ts.preprocessing(text=request.text)
        # Get word statistics
        word_stats = ts.statistics(token)

        # Validate Dataframe structure
        if word_stats.empty:
            raise HTTPException(status_code=500, detail="No words found after processing data")

        if 'words' not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure")

        return TextStatsResponse(status="success",
                                message="Text analysis completed successfully",
                                data=word_stats.set_index('words').to_dict('dict'))
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input text: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing text.")

@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    try:
        data = await file.read()
        text = data.decode("utf-8") # Convert bytes to string
        # Validate input text
        if text.strip() == "":
            raise HTTPException(status_code=400, detail="Input text must not be empty or whitespace-only")

        # Preprocessing data
        token = ts.preprocessing(text=text)
        # Get word statistics
        word_stats = ts.statistics(token)

        # Validate Dataframe structure
        if word_stats.empty:
            raise HTTPException(status_code=500, detail="No words found after processing data")

        if 'words' not in word_stats.columns:
            raise HTTPException(status_code=500, detail="Invalid Dataframe structure")

        return TextStatsResponse(status="success",
                                 message="Text analysis completed successfully",
                                 data=word_stats.set_index('words').to_dict('dict'))
    except UnicodeDecodeError:
        print("The uploaded file could not be read.")
        raise HTTPException(status_code=400, detail="The uploaded file could not be read.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error raised while analyzing the input file: {e}")
        raise HTTPException(status_code=500, detail="Error while analyzing file.")
