import streamlit as st
import PyPDF2
import docx
import spacy

# load spaCy model
nlp = spacy.load("en_core_web_sm")

st.title("📄 AI Resume Screener")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    text = ""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    # NLP processing
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]

    st.subheader("📌 Extracted Resume Text")
    st.write(text[:1000] + "..." if len(text) > 1000 else text)

    st.subheader("📊 Keywords")
    st.write(tokens[:30])
