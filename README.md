# InformationRetreivalSearchEngine
Search engine which searches data from the list of files based on the keyword passed.

The file aesopa10.txt contains some fables by the Greek poet Aesop. Splits the text document
so that each fable is placed in its own text file.

Implements a stop word removal function for your original documents. For a list of English
stop words, see the file englishST.txt3. The internal processing of the
documents is case-insensitive. Removes punctuation and line breaks.

Implemented a linear search in the document collection using a single search term. Linear search here means that you check sequentially for each individual document in the
collection whether the search term is contained (→ Boolean retrieval model).
Specify whether either the original documents or the stop-wordcleaned documents are used for the search.

Implemented a stemming function that uses the Porter algorithm. 
It also works with original document or the stop word removed documents.

Implemented the search using the vector space model and inverted lists!
