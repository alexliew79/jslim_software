#import streamlit
#import streamlit as st
import docx
import spacy

# Iterate over the entities in the processed text
#st.title("Quotation Processor")

# Load the large English NLP model
nlp = spacy.load("en_core_web_sm")


# Open the Word document
doc = docx.Document(r'C:\Users\Alex Liew\PycharmProjects\pythonProject2\Quote1.docx')

# Access the paragraphs in the document
for paragraph in doc.paragraphs:
    doc = nlp(paragraph.text
    print(doc)