import docx2txt
import PyPDF4
import io

from tkinter import *
from tkinter import filedialog



from retrieve_examples import search_document, display_results


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt'), ('Word documents', '*.docx'), ('PDF files', '*.pdf')])
    return file_path


print("Please select a document to search:")
document_path = select_file()
    # return doc_path

# document_path = input_document()

# Load text file
if document_path.endswith('.txt'):
    with open(document_path, 'r') as f:
        document_text = f.read()

# Load Word document using docx2txt library
elif document_path.endswith('.docx'):
    document_text = docx2txt.process(document_path)

 # Load PDF document using PyPDF4 library
elif document_path.endswith('.pdf'):
        with open(document_path, 'rb') as f:
            pdf_reader = PyPDF4.PdfFileReader(f)
            num_pages = pdf_reader.getNumPages()
            output = io.StringIO()
            for i in range(num_pages):
                page = pdf_reader.getPage(i)
                output.write(page.extractText())
            document_text = output.getvalue()

else:
    raise Exception("Error: Unsupported file format.")
    # print("Error: Unsupported file format.")

# Prompt user to enter a search term
search_term = input("Please enter a word/phrase/semantic unit to search for:")

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     input_document()

# Search the document for matching sentences
matching_sentences = search_document(document_text, search_term)

print(matching_sentences)

display_results(matching_sentences)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
