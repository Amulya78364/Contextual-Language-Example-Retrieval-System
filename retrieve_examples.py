import re
from tkinter import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from inflect import engine

# results_text = None

# Preprocess the document and return matching sentences
def search_document(document_text, search_term):
    if document_text == "":
        raise Exception("Error: input document is empty")

    if search_term == "":
        raise Exception("Error: search term is empty")

    # Preprocess the document text
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(document_text.lower())
    preprocessed_sentences = []
    p = engine()

    # Lemmatize and singularize the search term
    search_term = lemmatizer.lemmatize(search_term.lower())
    if p.singular_noun(search_term):
        search_term = p.singular_noun(search_term)

    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
        preprocessed_sentence = ' '.join(words)
        plural_words = []
        for word in words:
            plural_word = p.plural(word)
            if plural_word != word:
                plural_words.append(plural_word)
        plural_sentence = preprocessed_sentence
        for plural_word in plural_words:
            plural_sentence = re.sub(r"\b" + re.escape(plural_word) + r"\b", plural_word + "###", plural_sentence)
        preprocessed_sentences.append(plural_sentence)
        # preprocessed_sentences.append(preprocessed_sentence)

    # Vectorize the preprocessed sentences using TF-IDF
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(preprocessed_sentences)

    # Calculate the cosine similarity between the search term and each sentence
    search_term_vector = vectorizer.transform([search_term])
    similarities = cosine_similarity(search_term_vector, sentence_vectors).flatten()

    # Sort the sentences by similarity
    sorted_indices = similarities.argsort()[::-1]

    # Retrieve the sentences containing the search term
    matching_sentences = []
    for index in sorted_indices:
        # if re.search(r"\b" + re.escape(search_term) + r"\b", sentences[index]):
        if re.search(r"\b(" + re.escape(search_term) + r"|###+)\b", preprocessed_sentences[index]):
            original_sentence = sentences[index]
            retrieved_words = re.findall(r"\b" + re.escape(search_term) + r"\b", original_sentence)
            if not retrieved_words:
                retrieved_words = re.findall(r"\b###" + re.escape(search_term) + r"\b", original_sentence)
            matching_sentence = {
                'original': original_sentence,
                'retrieved': retrieved_words
            }
            matching_sentences.append(matching_sentence)

    return matching_sentences


# Display the search results with highlighted sentences
def display_results(matching_sentences):
    root = Tk()
    root.title("Matching Sentences")
    root.geometry("800x800")

    # global results_text

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    results_text = Text(root, yscrollcommand=scrollbar.set, font=("Times New Roman", 12))

    # Configure tag for highlighting
    results_text.tag_configure("highlight", background="red")

    for sentence in matching_sentences:
        original_sentence = sentence['original']
        retrieved_words = sentence['retrieved']
        highlighted_sentence = re.sub(r"\b(" + "|".join(retrieved_words) + r")\b", r"\1", original_sentence,
                                      flags=re.IGNORECASE)

        # Insert sentence into text widget
        results_text.insert(END, highlighted_sentence)

        # Highlight retrieved words in red
        for word in retrieved_words:
            start_index = "1.0"
            while True:
                start_index = results_text.search(word, start_index, END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                results_text.tag_add("highlight", start_index, end_index)
                start_index = end_index

        # Add separator line between sentences
        results_text.insert(END, "\n\n")

        return results_text
    root.mainloop()

    # results_text.pack(side=TOP, fill=BOTH, expand=TRUE)
    # scrollbar.config(command=results_text.yview)

    # root.mainloop()

    return results_text

