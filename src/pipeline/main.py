import text_stats as ts

def main():
    # Import data from TEXT file
    text = ts.import_data(filename='sample.txt', rootpath='data')

    # Preprocessing data
    token = ts.preprocessing(text)
    
    # Get word statistics
    word_stats = ts.statistics(token)

    # Export to CSV
    ts.export_results(word_stats, "word_frequency.csv", "output")

    # Visualize the results
    ts.visualize_results(word_stats, "word_frequency.png", "output")

if __name__ == "__main__":
    main()
