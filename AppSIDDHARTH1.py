from langchain import HuggingFaceHub
from langchain_community.llms import HuggingFaceHub
from fpdf import FPDF
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import streamlit as st
from io import BytesIO
st.title("HELLO!!!! 😎")
st.video(data="hellovi.mp4" ,format="hellovi.mp4", start_time=0,  subtitles=None, end_time=5, loop=True, autoplay=True, muted=True)
st.title(" I am A Text Summarizer 🤖")
st.warning("the text language should be 'ENGLISH'👁️👁️")

# Text cleaning function
def clean_text(text):
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201C": '"',
        "\u201D": '"',
        "\u2013": "-",
        "\u2014": "-",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

# PDF creation function 
def create_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", size=25)
    
    # Add title to PDF
    pdf.cell(0, 20, "TEXT", ln=True, align="C")
    
    # Add summary text
    pdf.set_font("Arial", size=12)
    cleaned_summary = clean_text(summary)
    pdf.multi_cell(0, 10, cleaned_summary)
    
    # Save PDF to a BytesIO stream
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer, "F")
    pdf_buffer.seek(0)
    return pdf_buffer

# Prediction function
def predict(text):
    llm =HuggingFaceHub(repo_id="utrobinmv/t5_summary_en_ru_zh_base_2048", model_kwargs={"temperature":0,"max_length":64} )
    prompt =PromptTemplate(input_variables=['text'], template='give the summary of given text in English:{text}')
    chain = LLMChain(llm=llm, prompt=prompt)
    summary = chain.run(text)
    return summary

# User input
input_text = st.text_area("Enter the text you want to summarize:")

# Summarize button and download options
if st.button("Summarize"):
    summary = predict(input_text)
    st.write("Summary of your Given text is:")
    st.write(summary)
    st.write("Download options")
    st.info("GOOD news YOU CAN DOWNLOAD the pdf and txt file of the summary !!!")
    # Download buttons
    txt_button = st.download_button(
        "Download as TXT", data=summary, file_name="Summary.txt", mime="text/plain"
    )
    pdf_button = st.download_button(
        "Download as PDF", data=create_pdf(summary), file_name="Summary.pdf", mime="application/pdf"
    )
