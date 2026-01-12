# Mini-Project: Word Frequency Statistics in Text

## Objective

Write a Python program that takes any text input, preprocesses it (by removing punctuation, special characters, and stopwords) to extract meaningful words, counts the frequency of each word, and outputs the results to the screen or saves them to a file. The preprocessing step is essential to ensure accurate word frequency analysis by eliminating noise and focusing on significant terms.

## Detailed Requirements

### Input

- A text passage (or load from a .txt file).
- The text can be in Vietnamese or English.

### Text Processing

- Convert all text to lowercase.
- Remove punctuation and special characters (keep only letters and numbers).
- Split the text into individual words (tokenization).

### Statistics

- Count the number of occurrences of each word in the text.
- Store the results in a suitable data structure (e.g., dict or Counter).

### Output

- Print the list of words with their frequencies (sorted in descending order of frequency).
- Optionally: save the results to a .csv or .txt file.

### Advanced Requirements (Optional)

- Remove stopwords if the text is in English or Vietnamese.
- Visualize the results with a chart (using matplotlib).
- Count phrase frequencies (bigram/trigram).
- Write functions to allow direct text input from the keyboard or from a file.

## Example Input

```
Xin chào! Đây là ví dụ về dự án nhỏ. Xin chào mọi người.
```

## Example Output

```
'chào': 2
'xin': 2
'đây': 1
'ví': 1
'dụ': 1
```

## Final Requirement

- Write Python code that meets the above requirements.
- Ensure the code is easy to understand, with comments explaining each step.
- The code should work with various texts.

---

## CI/CD Pipeline

This project includes automated Continuous Integration and Continuous Deployment (CI/CD) workflows using GitHub Actions.

### CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:** Push to `main` branch or `releases/**` branches

**Workflow Steps:**

1. **Run Linters**

   - Python version: 3.13
   - Tools: `black` (code formatter) and `flake8` (style checker)
   - Ensures code quality and style consistency

2. **Run Tests**

   - Python versions tested: 3.9, 3.10, 3.11, 3.12, 3.13
   - Runs all unit tests using `unittest`
   - Generates code coverage reports using `coverage`
   - Matrix strategy ensures compatibility across Python versions

3. **Build Docker Image**
   - Only runs on push to `main` branch
   - Builds Docker image and pushes to GitHub Container Registry (ghcr.io)
   - Supports multi-architecture builds (QEMU + Docker Buildx)

### CD Pipeline (`.github/workflows/cd.yml`)

**Triggers:** Successful completion of CI workflow on `main` branch

**Workflow Steps:**

1. **Deploy to Production**
   - Environment: Production
   - Deployment target: Render (via deploy hook)
   - Requires `RENDER_DEPLOY_HOOK_URL` secret in repository settings

### Running Tests Locally

```bash
# Run all tests
python -m unittest discover tests

# Run tests with coverage
python -m coverage run -m unittest
python -m coverage report -m

# Run specific test file
python -m unittest tests.test_text_stats

# Run specific test case
python -m unittest tests.test_text_stats.TestTextStats.test_import_data_returns_string
```

### CI/CD Requirements

**GitHub Secrets Required:**

- `RENDER_DEPLOY_HOOK_URL`: Render deployment webhook URL (for CD)

**GitHub Variables Required:**

- `RENDER_APP_URL`: Production application URL (for environment tracking)

### Badge Status

You can add these badges to track CI/CD status:

```markdown
![CI Status](https://github.com/YOUR_USERNAME/word-frequency-mini-project/workflows/CI%20-%20Tests%20&%20Quality%20Checks/badge.svg)
![CD Status](https://github.com/YOUR_USERNAME/word-frequency-mini-project/workflows/CD%20-%20Continuous%20Deployment/badge.svg)
```

---

## 🚀 Getting Started - Quick Guide

### Step 1: Prerequisites

**Required Software:**

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Visual Studio Code** (recommended) or any text editor

**Check your Python installation:**

```bash
python --version
pip --version
```

### Step 2: Quick Start (Easiest!)

**Just run the startup script:**

```bash
# Windows
start.bat

# Or use Python directly (cross-platform)
python start.py

# Linux/Mac
chmod +x start.sh
./start.sh
```

This automated script will:

- ✅ Create all necessary directories
- ✅ Create required `__init__.py` files
- ✅ Check and optionally install dependencies
- ✅ Download NLTK data
- ✅ Start the FastAPI server automatically

**That's it!** The server will start at `http://localhost:5000`

---

### Step 2 (Alternative): Manual Setup

**1. Clone or download this repository:**

```bash
# If using Git
git clone <repository-url>
cd word-frequency-mini-project

# Or download ZIP and extract it
```

**2. Create virtual environment (Recommended):**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

**3. Install all dependencies:**

```bash
pip install -r requirements.txt
```

**4. Download required NLTK data:**

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 3: Verify Project Structure

**Ensure you have these essential `__init__.py` files:**

```
word-frequency-mini-project/
├── src/
│   ├── __init__.py          ⚠️ REQUIRED!
│   ├── app/
│   │   ├── __init__.py      ⚠️ REQUIRED!
│   │   ├── main.py
│   │   ├── models.py
│   │   └── middleware.py
│   └── pipeline/
│       ├── __init__.py      ⚠️ REQUIRED!
│       └── text_stats.py
├── data/                    # Input text files
├── output/                  # Output files (auto-created)
├── requirements.txt
└── README.md
```

**Create missing `__init__.py` files if needed:**

```bash
# Windows PowerShell
New-Item -ItemType File -Path "src\__init__.py" -Force
New-Item -ItemType File -Path "src\app\__init__.py" -Force
New-Item -ItemType File -Path "src\pipeline\__init__.py" -Force

# Linux/Mac
touch src/__init__.py
touch src/app/__init__.py
touch src/pipeline/__init__.py
```

### Step 4: Create Required Directories

```bash
# Create output directory if it doesn't exist
mkdir output
```

### Step 5: Run the Application

**Option A: Run FastAPI Web Server (Recommended)**

```bash
# From project root directory
uvicorn src.app.main:app --reload --port 5000
```

**Option B: Run using Python module**

```bash
# From project root directory
python -m src.app.main
```

**Access the API:**

- Open browser: `http://localhost:5000/docs` (Swagger UI)
- API will be available at: `http://localhost:5000`

### Step 6: Test the API

**Using Swagger UI (Easiest):**

1. Go to `http://localhost:5000/docs`
2. Try the `/analyses/text` endpoint
3. Click "Try it out"
4. Enter sample text and format
5. Click "Execute"

**Using curl (Command Line):**

```bash
# Test text analysis
curl -X POST "http://localhost:5000/analyses/text" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Xin chào! Đây là ví dụ về dự án nhỏ. Xin chào mọi người.\", \"format\": \"json\"}"

# Test file upload
curl -X POST "http://localhost:5000/analyses/file" \
  -F "file=@data/sample.txt" \
  -F "format=json"
```

**Using Python requests:**

```python
import requests

# Analyze text
response = requests.post("http://localhost:5000/analyses/text",
    json={"text": "Hello world! This is a test.", "format": "json"})
print(response.json())

# Analyze file
with open("data/sample.txt", "rb") as f:
    response = requests.post("http://localhost:5000/analyses/file",
        files={"file": f},
        data={"format": "csv"})
    with open("output/result.csv", "wb") as out:
        out.write(response.content)
```

---

## 📋 Usage Guide

### Method 1: Using the FastAPI Web Service

**Endpoints:**

1. **POST `/analyses/text`** - Analyze text directly

   ```json
   {
     "text": "Your text here",
     "format": "json" // Options: json, csv, png
   }
   ```

2. **POST `/analyses/file`** - Upload and analyze text file
   - Upload a `.txt` file (UTF-8 encoded)
   - Choose format: `json`, `csv`, or `png`

### Method 2: Using Core Pipeline Functions

```python
from src.pipeline import text_stats as ts

# Load data from file
text = ts.import_data("sample.txt", "data")

# Process text and get word frequencies
tokens = ts.preprocessing(text)
word_stats = ts.statistics(tokens)

# Export results to CSV
ts.export_results(word_stats, "word_frequency.csv", "output")

# Visualize results
ts.visualize_results(word_stats, "word_frequency.png", "output")
```

### File Structure

```
word-frequency-mini-project/
├── src/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Pydantic models
│   │   └── middleware.py    # Custom middleware
│   └── pipeline/
│       ├── __init__.py
│       └── text_stats.py    # Core processing functions
├── data/                    # Input text files
├── output/                  # Output CSV/PNG files
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### Features

- **Bilingual Support**: Processes both English and Vietnamese text using NLTK and underthesea
- **Smart Stopword Removal**: Removes common words (179 English + 264+ Vietnamese stopwords)
- **Multiple Output Formats**: JSON, CSV, and PNG visualization
- **RESTful API**: FastAPI-based web service with Swagger documentation
- **File Upload Support**: Process text files directly
- **Flexible Input**: Load from .txt files or process strings directly
- **Encoding Support**: Properly handles UTF-8 Vietnamese diacritics and special characters
- **Security Middleware**: File size limits (5MB) and content type validation

### Example

**Input text:**

```
Xin chào! Đây là ví dụ về dự án nhỏ. Xin chào mọi người.
```

**Output CSV:**

```csv
words,counts
chào,2
xin,2
đây,1
ví,1
dụ,1
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **ModuleNotFoundError: No module named 'src'**

**Solution:**

- Ensure you're running from the project root directory
- Make sure all `__init__.py` files exist
- Use correct command: `uvicorn src.app.main:app` or `python -m src.app.main`

#### 2. **ImportError: attempted relative import beyond top-level package**

**Solution:**

- Check that `__init__.py` files exist in `src/`, `src/app/`, and `src/pipeline/`
- Run using: `python -m src.app.main` (not `python src/app/main.py`)

#### 3. **underthesea installation fails on Windows**

**Solution:**

- Install Visual Studio Build Tools: [Download here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
- Or install pre-built wheel: `pip install underthesea --prefer-binary`

#### 4. **NLTK data not found (punkt, stopwords)**

**Solution:**

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

#### 5. **Encoding errors with Vietnamese text**

**Solution:**

- Ensure input files are saved as UTF-8
- In VS Code: Check bottom-right corner → should say "UTF-8"
- If needed, use `utf-8-sig` encoding for BOM handling

#### 6. **Port 5000 already in use**

**Solution:**

```bash
# Use different port
uvicorn src.app.main:app --port 8000

# Or kill process using port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

#### 7. **Empty output after processing**

**Solution:**

- Check if input file exists and is not empty
- Verify file is UTF-8 encoded
- Ensure text contains valid words (not all stopwords)
- Check `output/` directory permissions

#### 8. **FileNotFoundError: output directory not found**

**Solution:**

```bash
mkdir output
```

#### 9. **Virtual environment not activating**

**Solution:**

```bash
# Windows - if execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
venv\Scripts\activate
```

---

## 💡 Pro Tips

1. **Use virtual environment** to avoid dependency conflicts
2. **Check API docs** at `http://localhost:5000/docs` for interactive testing
3. **Start with JSON format** for debugging, then switch to CSV/PNG
4. **Test with small text samples** before processing large files
5. **Keep output directory clean** - old files are not auto-deleted
6. **Monitor console logs** for detailed error messages

---

## 📞 Need Help?

If you encounter issues not listed here:

1. Check console/terminal error messages
2. Verify all installation steps were completed
3. Ensure Python version is 3.8+
4. Review API documentation at `/docs` endpoint
5. Check file paths and permissions
