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
'là': 1
'ví': 1
'dụ': 1
'về': 1
'dự': 1
'án': 1
'nhỏ': 1
'mọi': 1
'người': 1
```

## Final Requirement

- Write Python code that meets the above requirements.
- Ensure the code is easy to understand, with comments explaining each step.
- The code should work with various texts.

---

## How to Use

### Prerequisites

1. Install Python 3.8 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd word-frequency-mini-project
   ```

### Usage

#### Method 1: Using the main script

```bash
python src/main.py
```

This will process sample text and generate word frequency statistics in the output folder.

#### Method 2: Using individual functions

```python
import src.text_stats as ts

# Load data from file
text = ts.import_data("sample.txt", "data")

# Process text and get word frequencies
tokens = ts.preprocessing(text)
word_stats = ts.statistics(tokens)

# Export results to CSV
ts.export_data(word_stats, "word_frequency.csv", "output")
```

### File Structure

```
word-frequency-mini-project/
├── src/
│   ├── main.py              # Main execution script
│   └── text_stats.py        # Core functions
├── data/                    # Input text files
├── output/                  # Output CSV files
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### Features

- **Bilingual Support**: Processes both English and Vietnamese text using NLTK and underthesea
- **Smart Stopword Removal**: Removes common words (179 English + 264+ Vietnamese stopwords)
- **CSV Export**: Outputs structured data with 'words' and 'amount' columns for analysis
- **Flexible Input**: Load from .txt files or process strings directly
- **Encoding Support**: Properly handles UTF-8 Vietnamese diacritics and special characters
- **Pattern Matching**: Load multiple stopword files using glob patterns

### Example

Input text:

```
Xin chào! Đây là ví dụ về dự án nhỏ. Xin chào mọi người.
```

Output CSV:

```csv
words,amount
chào,2
xin,2
đây,1
ví,1
dụ,1
```

## Troubleshooting

### Common Issues

1. **underthesea installation fails on Windows**:

   - Install Visual Studio Build Tools
   - Or use the fallback Vietnamese stopwords list

2. **Encoding errors with Vietnamese text**:

   - Ensure input files are saved as UTF-8
   - Use `utf-8-sig` encoding if BOM issues occur

3. **Empty output**:
   - Check if input file exists in the correct path
   - Verify file is not empty after stopword removal
