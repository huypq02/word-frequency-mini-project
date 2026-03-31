# Word Frequency Analysis Engine

Simple Python project for word frequency analysis in English and Vietnamese.

## Overview

This project provides a small NLP pipeline and a REST API to analyze text frequency.

- Input: raw text or UTF-8 `.txt` file
- Processing: normalize text, tokenize, remove English and Vietnamese stopwords
- Output: frequency results as `json`, downloadable `csv`, or `png` chart
- Modes: use via FastAPI endpoints or import pipeline functions directly

It can:

- Process raw text or uploaded text files
- Remove punctuation and stopwords
- Count word frequency
- Return results as JSON, CSV, or PNG

## Project Structure

```text
.
├── src/
│   ├── app/                        # FastAPI layer
│   │   ├── main.py
│   │   ├── models.py
│   │   └── middleware.py
│   ├── pipeline/                   # Text processing pipeline
│   │   ├── text_stats.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── config/
│   │   └── constant.py
│   └── __init__.py
├── tests/
│   ├── test_text_stats.py
│   └── __init__.py
├── data/
│   ├── sample.txt
│   ├── non-utf-8-sample.txt
│   ├── vi_stopwords.txt
│   └── vietnamese_stopwords.txt
├── output/                         # Generated CSV/PNG results
├── requirements.txt
├── Dockerfile
├── start.py
├── start.sh
├── start.bat
└── README.md
```

## Requirements

- Python 3.8+

## Quick Start

```bash
python start.py
```

This bootstraps the environment and starts the API at `http://localhost:5000`.

## Manual Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
uvicorn src.app.main:app --reload --port 5000
```

API docs: `http://localhost:5000/docs`

## API Examples

### Analyze Raw Text

```bash
curl -X POST "http://localhost:5000/analyses/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "output_format": "json"}'
```

### Analyze Uploaded File

```bash
curl -X POST "http://localhost:5000/analyses/file" \
  -F "file=@data/sample.txt" \
  -F "output_format=csv"
```

Supported formats: `json`, `csv`, `png`.

## Python Usage

```python
from src.pipeline import text_stats as ts

text = ts.import_data("sample.txt", "data")
tokens = ts.preprocessing(text)
word_stats = ts.statistics(tokens)
ts.export_results(word_stats, "results.csv", "output")
```

## Testing

```bash
python -m unittest discover tests
```

Optional coverage:

```bash
python -m coverage run -m unittest
python -m coverage report
```

## Notes

- Vietnamese tokenization uses `underthesea`
- Input files must be UTF-8 text
- Very large files are not optimized for memory usage
