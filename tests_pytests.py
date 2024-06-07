import unittest

from tkinter import Text, END
from retrieve_examples import search_document, display_results


# pytest to handle if empty input document is provided
def test_empty_input_document():
    document_text = ''
    search_term = 'test'
    try:
        search_document(document_text, search_term)
    except Exception as e:
        expected_exception = 'Error: input document is empty'
        assert str(e) == expected_exception


# pytest to handle if search term is not provided
def test_empty_search_term():
    document_text = 'This is a test sentence. Here is another test sentence.'
    search_term = ''
    try:
        search_document(document_text, search_term)
    except Exception as e:
        expected_exception = 'Error: search term is empty'
        assert str(e) == expected_exception


def test_search_document_no_matching_sentences():
    document_text = "This is the first sentence. This is the second sentence. The second sentence has the word " \
                    "'sentence' twice."
    search_term = 'apple'
    actual_output = search_document(document_text, search_term)
    assert actual_output == []


def test_search_document_one_matching_sentence():
    document_text = "The book on the shelf is full of interesting stories. The computer on the desk is running slowly."
    search_term = "book"
    expected_output = [
        {
            "original": "the book on the shelf is full of interesting stories.",
            "retrieved": ["book"]
        }
    ]
    assert search_document(document_text, search_term) == expected_output


def test_search_document_case_insensitivity():
    document_text = "The book on the shelf is full of interesting stories. The computer on the desk is running slowly."
    search_term = "BOOK"
    expected_output = [
        {
            "original": "the book on the shelf is full of interesting stories.",
            "retrieved": ["book"]
        }
    ]
    assert search_document(document_text, search_term) == expected_output


def test_search_document():
    document_text = 'This is a test sentence. Here is another test sentence.'
    search_term = 'test'
    expected_output = [{'original': 'this is a test sentence.', 'retrieved': ['test']},
                       {'original': 'here is another test sentence.', 'retrieved': ['test']}]

    actual_output = search_document(document_text, search_term)
    assert actual_output == expected_output


def test_number_search_document_positive():
    document_text = 'This is a test sentence. Here is another test sentence.'
    search_term = 'test'
    actual_output = search_document(document_text, search_term)
    actual_len = len(actual_output)
    expected_len = 2
    assert actual_len == expected_len


def test_number_search_document_negative():
    document_text = 'This is a test sentence. Here is another test sentence.'
    search_term = 'test'
    actual_output = search_document(document_text, search_term)
    actual_len = len(actual_output)
    expected_len = 3
    assert actual_len != expected_len


# pytest to handle plural forms - if search term is given in singular form
def test_search_document_pluralization():
    document_text = 'The flower in the vase is a beautiful shade of red. Some popular flowers include roses, daisies, ' \
                    'and tulips.' \
                    ' The computer on the desk is running slowly.'
    search_term = 'flower'
    expected_output = ['the flower in the vase is a beautiful shade of red.',
                       'some popular flowers include roses, daisies, and tulips.']
    actual_output = search_document(document_text, search_term)
    original_sentences = [dictionary['original'] for dictionary in actual_output]
    assert original_sentences == expected_output


# pytest to handle singular forms - if search term is given in plural form
def test_search_document_singularization():
    document_text = 'The flower in the vase is a beautiful shade of red. Some popular flowers include roses, daisies, ' \
                    'and tulips.' \
                    ' The computer on the desk is running slowly.'
    search_term = 'flowers'
    expected_output = ['the flower in the vase is a beautiful shade of red.',
                       'some popular flowers include roses, daisies, and tulips.']
    actual_output = search_document(document_text, search_term)
    original_sentences = [dictionary['original'] for dictionary in actual_output]
    assert original_sentences == expected_output


# Test case for empty matching sentences list
def test_display_results_empty():
    matching_sentences = []
    results_text = display_results(matching_sentences)
    # Check if text widget is empty
    assert results_text.get("1.0", END) == "\n"