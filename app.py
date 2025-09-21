import streamlit as st
import PyPDF2
import docx
import spacy
import subprocess
import sys

# Ensure the spaCy model is available; download if not present
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("📄 AI Resume Screener")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    text = ""
    # PDF
    if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    # DOCX
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.lower().endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        st.error("Unsupported file type. Use PDF or DOCX.")

    if text.strip() == "":
        st.warning("No text extracted from the file.")
    else:
        # Use spaCy to extract basic keywords/tokens
        doc = nlp(text)
        tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]

        st.subheader("📌 Extracted Resume Text")
        st.write(text[:2000] + "..." if len(text) > 2000 else text)

        st.subheader("📊 Top Keywords (first 40)")
        st.write(tokens[:40])
