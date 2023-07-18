import os
import re
import porter_stemming


# Method to format name of the file using fable name
def format_fable_name(heading):
    formatted_name = heading.lower()
    formatted_name = formatted_name.replace(' ', '_')
    formatted_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in formatted_name)
    formatted_name = formatted_name.strip('_\',')
    return formatted_name


# Method to remove stop words
def remove_stop_words(text_original, stop_words):
    words = text_original.split()
    cleaned_words = [word for word in words if word.lower() not in stop_words]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text


# Method to remove punctuation
def remove_punctuation(text_after_stop_words):
    cleaned_text = re.sub(r'[^\w\s\'-]', '', text_after_stop_words)
    cleaned_text = cleaned_text.replace('\n', ' ')
    return cleaned_text


# Method to output the final search documents
def result_documents(output_documents):
    for doc_name in sorted(output_documents):
        print(doc_name)


# Linear search
def linear_search(query, folder_path, stem_flag):
    query = query.lower()
    matching_files = []
    if stem_flag:
        stemmer_object = porter_stemming.PorterStemmer()
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            stemmed_words_in_file = []
            with open(filepath, 'r') as file:
                content = file.read()
            words = content.split()
            for word in words:
                stemmed_words_in_file.append(stemmer_object.stem(word))
            if '&' in query:
                parts = query.split('&')
                if stemmer_object.stem(parts[0]) in stemmed_words_in_file and stemmer_object.stem(parts[1]) \
                        in stemmed_words_in_file:
                    matching_files.append(filename)
            elif '|' in query:
                parts = query.split('|')
                if stemmer_object.stem(parts[0]) in stemmed_words_in_file or stemmer_object.stem(parts[1]) \
                        in stemmed_words_in_file:
                    matching_files.append(filename)
            elif '!' in query:
                parts = query[1:]
                if stemmer_object.stem(parts) not in stemmed_words_in_file:
                    matching_files.append(filename)
            elif stemmer_object.stem(query) in stemmed_words_in_file:
                matching_files.append(filename)

    else:
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                content = file.read()
            if '&' in query:
                parts = query.split('&')
                if parts[0].lower() in content.lower() and parts[1].lower() in content.lower():
                    matching_files.append(filename)
            elif '|' in query:
                parts = query.split('|')
                if parts[0].lower() in content.lower() or parts[1].lower() in content.lower():
                    matching_files.append(filename)
            elif '!' in query:
                parts = query[1:]
                if parts not in content.lower():
                    matching_files.append(filename)
            elif query.lower() in content.lower():
                matching_files.append(filename)
    result_documents(set(matching_files))
    return matching_files


def inverted_list_generation(query, folder_path):
    matching_files = []
    unique_words = {}
    # Iterate over each file in the directory
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        # Read the contents of the file
        with open(filepath, 'r') as file:
            content = file.read()
            content = remove_punctuation(content)
        # Split the content into words
        words = content.lower().split()

        # Update the unique words dictionary
        for word in words:
            if word in unique_words:
                unique_words[word].add(filename)
            else:
                unique_words[word] = {filename}
    return unique_words


# Inverted search
def inverted_list(query, folder_path):
    unique_words = inverted_list_generation(query, folder_path)
    if '&' in query:
        parts = query.split('&')
        if parts[0].lower() in unique_words and parts[1].lower() in unique_words:
            matching_files = unique_words[parts[0].lower()] & unique_words[parts[1].lower()]
    elif '|' in query:
        parts = query.split('|')
        if parts[0].lower() in unique_words or parts[1].lower() in unique_words:
            matching_files = unique_words[parts[0].lower()] | unique_words[parts[1].lower()]
    elif '!' in query:
        parts = query[1:]
        if parts in unique_words:
            all_documents = set().union(*unique_words.values())
            matching_files = all_documents - unique_words[parts]
        else:
            matching_files = set(unique_words.keys())
    elif query.lower() in unique_words:
        matching_files = unique_words.get(query.lower())
    result_documents(matching_files)
    return matching_files


def calculate_precision_recall(query, retrieved_docs, total_time):
    retrieved_docs_list = [int(word[1]) if word[0] == '0' else int(word[:2]) for word in retrieved_docs]
    relevant_docs_list = []
    query = query.lower()
    with open('ground_truth.txt', 'r') as file:
        content = file.read()
        lines = content.split('\n')
        gt_dict = {}
        for line in content.strip().split("\n"):
            # Split the line by hyphen to separate the first word and the numbers
            parts = line.strip().split(" - ")
            search_term = parts[0]
            numbers = [int(num) for num in parts[1].split(",")]
            # Store the first word and numbers in the dictionary
            gt_dict[search_term] = numbers
            if query in gt_dict:
                relevant_docs_list = gt_dict.get(query, [])
                break
        print(retrieved_docs_list)
        TP = len(set(relevant_docs_list) & set(retrieved_docs_list))
        FP = len(set(retrieved_docs_list) - set(relevant_docs_list))
        FN = len(set(relevant_docs_list) - set(retrieved_docs_list))

        precision = TP / (TP + FP) if (TP + FP) != 0 else 0
        recall = TP / (TP + FN) if (TP + FN) != 0 else 0

        if precision == 0 or recall == 0:
            print(f'T={total_time}ms, P = ?, R = ?')
        else:
            # Print the results
            print(f'T={total_time}ms, P = {round(precision, 2)}, R = {round(recall, 2)}')
