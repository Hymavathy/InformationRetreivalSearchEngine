import math
import os
import re
import sys
from collections import defaultdict
import numpy


def inverted_index_vector_space(folder_path):
    word_count = defaultdict(dict)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, 'r') as f:
                document = f.read()

                # Remove non-alphanumeric characters and convert to lowercase
                document = re.sub(r'[^a-zA-Z0-9\s]', '', document).lower()

                # Split the document into words
                words = document.split()

                # Count the frequency of each word
                word_frequency = defaultdict(int)
                for word in words:
                    word_frequency[word] += 1

                # Update the nested dictionary with word frequencies
                document_name = os.path.basename(file_path)
                for word, frequency in word_frequency.items():
                    if document_name in word_count[word]:
                        word_count[word][document_name] += frequency
                    else:
                        word_count[word][document_name] = frequency

    return word_count


# This function modifies the dictionary and replaces it with the logarithm values hence
# indirectly performing the product of tf and IDF here
def generate_idf_weights_product(total_documents, inverted_index_list_docs, query_count):
    for query_key, query_value in query_count.items():
        for inverted_index_key, nested_dict in inverted_index_list_docs.items():
            if query_key == inverted_index_key:
                query_count[query_key] = query_value * (round(numpy.log(total_documents / len(nested_dict)), 5))
            for nested_key, nested_value in nested_dict.items():
                inverted_index_list_docs[inverted_index_key][nested_key] = nested_value * (
                    round(numpy.log(total_documents / len(nested_dict)), 5))


def transform_dictionary(word_count):
    transformed_dict = {}

    for word, file_counts in word_count.items():
        for file, count in file_counts.items():
            if file not in transformed_dict:
                transformed_dict[file] = {}

            if word not in transformed_dict[file]:
                transformed_dict[file][word] = 0

            transformed_dict[file][word] = count

    return transformed_dict


def calculate_magnitude_of_documents(inverted_index_list_docs):
    magnitude_of_docs = {}
    for inverted_index_key, nested_dict in inverted_index_list_docs.items():
        magnitude = 0
        for nested_key, nested_value in nested_dict.items():
            magnitude = magnitude + nested_value * nested_value
        magnitude_of_docs[inverted_index_key] = round(math.sqrt(magnitude), 4)
    return magnitude_of_docs


def calculate_query_and_doc_product(transformed_dict, query_count):
    query_and_doc_product = {}
    for inverted_index_key, nested_dict in transformed_dict.items():
        sum_value = 0
        for nested_key, nested_value in nested_dict.items():
            for key, value in query_count.items():
                if key == nested_key:
                    sum_value = sum_value + (nested_value * value)
        query_and_doc_product[inverted_index_key] = round(sum_value, 4)
    return query_and_doc_product


def calculate_magnitude_of_query(query_count):
    magnitude = 0
    for key, value in query_count.items():
        magnitude = magnitude + (value * value)
    return round(math.sqrt(magnitude), 4)


def calculate_cosine_similarity(query_and_doc_product, magnitude_of_docs, magnitude_of_query):
    final_list_cosine = {}
    for key1, value1 in query_and_doc_product.items():
        for key2, value2 in magnitude_of_docs.items():
            if key1 == key2:
                final_list_cosine[key1] = round(value1 / (magnitude_of_query * value2), 5)
    return final_list_cosine


def display_documents_using_stdout(final_list_cosine):
    print_files = {}
    for key, value in final_list_cosine.items():
        if value > 0:
            print_files[key] = value
    sorted_words = sorted(print_files.items(), key=lambda x: x[1], reverse=True)
    for word, values in sorted_words:
        sys.stdout.write(f"{word}\n")


def vector_space_model(query, folder_path):
    word_list = query.split()
    query_count = {}
    for word in word_list:
        if word in query_count:
            query_count[word] += 1
        else:
            query_count[word] = 1

    total_documents = sum([len(files) for _, _, files in os.walk(folder_path)])
    inverted_index_list_docs = inverted_index_vector_space(folder_path)
    generate_idf_weights_product(total_documents, inverted_index_list_docs, query_count)
    transformed_dict = transform_dictionary(inverted_index_list_docs)
    magnitude_of_query = calculate_magnitude_of_query(query_count)
    query_and_doc_product = calculate_query_and_doc_product(transformed_dict, query_count)
    magnitude_of_docs = calculate_magnitude_of_documents(transformed_dict)
    final_list_cosine = calculate_cosine_similarity(query_and_doc_product, magnitude_of_docs, magnitude_of_query)
    display_documents_using_stdout(final_list_cosine)
