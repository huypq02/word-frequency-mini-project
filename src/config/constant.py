"""Centralized constants for the word frequency mini project."""

# Project metadata
PROJECT_NAME = "NLP Word Frequency Mini Project"
PROJECT_VERSION = "2.1.0"
PROJECT_AUTHOR = "Huy Pham"
PROJECT_EMAIL = "huypham0297@gmail.com"

# App and API constants
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
DEFAULT_LOG_LEVEL = "info"
APP_IMPORT_PATH = "src.app.main:app"

SUPPORTED_OUTPUT_FORMATS = ("json", "csv", "png")
DEFAULT_OUTPUT_FORMAT = "json"

ALLOWED_FILE_CONTENT_TYPES = ["text/plain"]
ALLOWED_CONTENT_TYPE_HEADERS = ["multipart/form-data", "application/json"]

# Data and output constants
DATA_DIR = "data"
OUTPUT_DIR = "output"
STOPWORDS_FILE_PATTERN = "*stopwords.txt"
OUTPUT_FILE_PREFIX = "word_frequency"

# Text processing constants
WORDS_COLUMN = "words"
COUNTS_COLUMN = "counts"
DEFAULT_TOP_N_WORDS = 10

