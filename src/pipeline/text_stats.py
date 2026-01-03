import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import underthesea
import matplotlib.pyplot as plt
import os
import glob

def import_data(filename, rootpath):
    """Load a text file from rootpath and return its contents as a DataFrame."""
    fullpath = os.path.join(rootpath, filename)
    data = ''
    if os.path.exists(fullpath):
        with open(fullpath, encoding='utf-8') as f:
            data = f.read()
    return data

def load_vi_stopwords(patternpath, rootpath):
    """Load Vietnamese stopwords from multiple txt files."""
    vi_stopwords = []
    for filepath in glob.glob(pathname=patternpath, root_dir=rootpath):
        fullpath = os.path.join(rootpath, filepath)
        if os.path.exists(fullpath):
            with open(fullpath, encoding='utf-8') as f:
                vi_stopwords.extend([line.strip() for line in f if line.strip()])
        else:
            print(f"File not found: {filepath}")
    return vi_stopwords

def preprocessing(text):
    """Return individual words after preprocessing."""
    # Lowercase and Punctual Removal
    text = re.sub("[^\w\s\-]", " ", text).lower()

    # Stop word removal
    # English
    en_stopwords = stopwords.words('english')
    # Vietnamese
    rootpath = 'data'
    pattern = '*stopwords.txt'
    vi_stopwords = load_vi_stopwords(pattern, rootpath)

    # Both English and Vietnamese Tokenization
    tokens = underthesea.word_tokenize(text)

    # Remove both English and Vietnamese stopwords
    tokens = [token for token in tokens if token not in en_stopwords and token not in vi_stopwords]
    return tokens

def statistics(tokens):
    """Return the number of occurrences of each word in the text."""
    # Using the unigrams to count the number of occurrences of each word 
    unigrams = (pd.Series(nltk.ngrams(tokens, 1)))

    # Convert unigrams from tuple to string
    nwords = unigrams.apply(
        lambda words: words[0]
    )
    
    # Define a Dataframe from nwords Series;
    # count the number of occurrences of each word and reset index
    df = nwords.value_counts().reset_index()
    df.columns = ['words', 'counts']

    return df

def export_results(dataset, filename, rootpath):
    """Export DataFrame to CSV file in the specified directory."""

    # Create new directory if it exists
    os.makedirs(rootpath, exist_ok=True)
    fullpath = os.path.join(rootpath, filename)

    # Declare the Dataframe from the dataset
    df = pd.DataFrame(dataset)

    # Use utf-8-sig to ensure proper encoding
    df.to_csv(fullpath, index=False, encoding='utf-8-sig')

def visualize_results(dataset, filename, rootpath, top_n=10):
    """Visualize the top N most frequent words from the dataset and save the plot as an image file."""

    # Create new directory if it exists
    os.makedirs(rootpath, exist_ok=True)
    fullpath = os.path.join(rootpath, filename)

    # Declare the Dataframe from the dataset
    df = pd.DataFrame(dataset)
    top_words = df.head(top_n)

    # Using matplotlib.pyplot to visualize the results 
    plt.figure(figsize=(12,6))
    plt.bar(top_words['words'], top_words['counts'])
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.savefig(fullpath, format='png')
    plt.show()