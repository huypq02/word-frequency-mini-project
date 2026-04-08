import text_stats as ts
from src.config.constant import DATA_DIR, OUTPUT_DIR

def main():
    # Import data from TEXT file
    text = ts.import_data(filename="sample.txt", rootpath=DATA_DIR)

    # Preprocessing data
    token = ts.preprocessing(text)
    
    # Get word statistics
    word_stats = ts.statistics(token)

    # Export to CSV
    ts.export_results(word_stats, "word_frequency.csv", OUTPUT_DIR)

    # Visualize the results
    ts.visualize_results(word_stats, "word_frequency.png", OUTPUT_DIR)

if __name__ == "__main__":
    main()
