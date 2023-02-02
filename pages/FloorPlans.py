import streamlit
import streamlit as st
import docx
import spacy
import random

# Iterate over the entities in the processed text
st.title("Quotation Processor")

# Load the large English NLP model
nlp = spacy.load("en_core_web_sm")


# Open the Word document
doc = docx.Document(r'C:\Users\Alex Liew\PycharmProjects\pythonProject2\Quote1.docx')

# Access the paragraphs in the document
for paragraph in doc.paragraphs:
    doc = nlp(paragraph.text)
    # The text to process
    for ent in doc.ents:
        # Check if the entity is a price
        if ent.label_ == "MONEY":
            # Extract the work description
            work = [token.text for token in doc if token.ent_type_ != "MONEY"][:-1]
            work = " ".join(work)
            # Extract the price
            price = ent.text


            # Print the extracted work and price
            streamlit.markdown(f"Work: {work}, Price: {price}" )

import spacy

# Load the pre-trained model
nlp = spacy.load("en_core_web_sm")

# Modify the pipeline to include the NER component
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe("ner")

# Prepare the training data
TRAIN_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "GPE"), (18, 24, "GPE")]}),
]

# Start the training process
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(100):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update([text], [annotations], sgd=optimizer, losses=losses)
        print(f"Losses at iteration {itn}: {losses}")

# Save the fine-tuned model to a directory
nlp.to_disk("/path/to/model_directory")


