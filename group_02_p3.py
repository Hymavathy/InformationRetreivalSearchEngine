import argparse
import os
import time
from method_implementation import remove_stop_words, remove_punctuation, format_fable_name, linear_search, \
    inverted_list, calculate_precision_recall
from vector_space_model import vector_space_model

parser = argparse.ArgumentParser(description='Extract fables from a text file and remove stop words.')
parser.add_argument('--extract-collection', metavar='FILE_NAME', help='Call document extraction on FILE_NAME')
parser.add_argument('--query', metavar='QUERY_TEXT', help='Specify a user query')
parser.add_argument('--model', choices=['bool', 'vector'], default='bool',
                    help='Set the model to Boolean or Vector space model')
parser.add_argument('--search_mode', choices=['linear', 'inverted'], default='linear',
                    help='Makes the Boolean search use an inverted list or linear search')
parser.add_argument('--stemming', action='store_true',
                    help='specifies that words in query and documents should be stemmed')
parser.add_argument('--documents', choices=['original', 'no_stopwords'], default='original',
                    help='Specify the source documents for the search')
args = parser.parse_args()

folder_path_original = os.path.join(os.getcwd(), 'collection_original')
if not os.path.exists(folder_path_original):
    os.makedirs(folder_path_original)

folder_path_no_stopwords = os.path.join(os.getcwd(), 'collection_no_stopwords')
if not os.path.exists(folder_path_no_stopwords):
    os.makedirs(folder_path_no_stopwords)

if args.extract_collection:
    delimiter = "Aesop's Fables\n\n\n\n"
    # Read the document from a file
    with open(args.extract_collection, 'r') as file:
        document = file.read()
    # Split the document into two parts using the delimiter
    parts = document.split(delimiter, 1)
    second_part = parts[1]
    # Save the second part into a temporary file
    with open('temp_file.txt', 'w') as temp_file:
        temp_file.write(second_part)

    with open('englishST.txt', 'r') as stop_words_file:
        stop_words = {word.strip().lower() for word in stop_words_file.readlines()}

    with open('temp_file.txt', 'r') as file:
        content = file.read()
        fables = content.split('\n\n\n\n')

        for i, fable in enumerate(fables):
            fable_lines = fable.strip().split('\n')
            fable_number = str(i + 1).zfill(2)
            title = fable_lines[0]
            formatted_title = format_fable_name(title)
            filename = f'{fable_number}_{formatted_title}.txt'

            filepath = os.path.join(folder_path_original, filename)
            with open(filepath, 'w') as fable_file:
                fable_file.write(fable)

            text = remove_stop_words(fable, stop_words)
            text = remove_punctuation(text)
            filepath_no_stop_words = os.path.join(folder_path_no_stopwords, filename)
            with open(filepath_no_stop_words, 'w') as fable_file:
                fable_file.write(text)

if args.model == 'bool':
    retrieved_docs = []
    folder_path = folder_path_no_stopwords if args.documents == 'no_stopwords' else folder_path_original
    if args.search_mode == 'linear':
        start_time = time.time()
        retrieved_docs = linear_search(args.query, folder_path, args.stemming)
        end_time = time.time()
        total_time = round((end_time - start_time) * 1000, 2)
    elif args.search_mode == 'inverted':
        start_time = time.time()
        retrieved_docs = inverted_list(args.query, folder_path)
        end_time = time.time()
        total_time = round((end_time - start_time) * 1000, 2)
    calculate_precision_recall(args.query, retrieved_docs, total_time)

if args.model == 'vector':
    folder_path = folder_path_no_stopwords if args.documents == 'no_stopwords' else folder_path_original
    vector_space_model(args.query, folder_path)
