import streamlit as st
import PyPDF2
import io 
from groq import Groq   
st.title("Summarizer")
client = Groq(api_key=st.secrets['Groq_Api_Key'])
st.write("Enter your text below to get a summary:")
file = st.file_uploader("Upload your text file", type=["pdf"])
if file is not None:
    pdf_reader= PyPDF2.PdfReader(io.BytesIO(file.read()))
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""
    if pdf_text.strip():
        st.info(f"Text extracted from the uploaded PDF: {len(pdf_reader.pages)} pages")
        text_from_pdf = pdf_text
    else:
        st.warning("No text found in the uploaded PDF.")
        text_from_pdf = ""
else:
    text_from_pdf = ""
text = st.text_area("Or paste your text here:", height=200 , value=text_from_pdf)
if st.button("Summarize"):
    if len(text.strip()) < 10:
        st.warning("Please enter at least 10 characters of text to summarize.")
    else:
        with st.spinner("Generating summary..."):
            arabic_letters = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
            lang = "Arabic" if arabic_letters > 10 else "English"
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"you are a helpful assistant, summarize the text into 4 simple sentences, in {lang} language."},
                    {"role": "user", "content": text}
                ]
            )
            st.success(response.choices[0].message.content)
