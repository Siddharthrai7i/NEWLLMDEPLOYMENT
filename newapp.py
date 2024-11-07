from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from fpdf import FPDF
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from dotenv import load_dotenv
import os
import streamlit as st
from io import BytesIO  # Import BytesIO to handle binary data


# load_dotenv() 
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def summarization(text):
    llm = HuggingFaceHub(repo_id="utrobinmv/t5_summary_en_ru_zh_base_2048", model_kwargs={"temperature":0,"max_length":64} )
    prompt = PromptTemplate(input_variables=['text'], template='give the summary of given text {text}')
    chain = LLMChain(llm=llm, prompt=prompt)
    summary = chain.run(text)
    return summary

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

def create_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", size=25)
    pdf.cell(0, 20, "SUMMARY", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    cleaned_summary = clean_text(summary)
    pdf.multi_cell(0, 10, cleaned_summary)

    pdf_buffer = BytesIO()  # Use BytesIO to store PDF in-memory
    pdf.output(pdf_buffer, "F")
    pdf_buffer.seek(0)  # Move to the beginning of the BytesIO buffer
    return pdf_buffer


st.title("HELLO!!!! 😎")
st.video(data="hellovi.mp4" ,format="hellovi.mp4", start_time=0,  subtitles=None, end_time=5, loop=True, autoplay=True, muted=True)
st.title(" I am A Text Summarizer 🤖")
st.warning("the text language should be 'ENGLISH'👁️👁️")

text = st.text_area("Enter the text to be summarized", height=200)

if st.button("Summarize"):
    if text:
        summary = summarization(text)
        if summary:
            st.subheader("Summary:")
            st.write(summary)
            st.write("Download options")
            st.info("GOOD news YOU CAN DOWNLOAD the pdf and txt file of the summary !!!")
            
            st.write("Download options:")
            
            # Download as TXT
            st.download_button(
                "Download as TXT", data=summary, file_name="summary.txt", mime="text/plain"
            )
            
            # Download as PDF
            pdf_data = create_pdf(summary)
            st.download_button(
                "Download as PDF", data=pdf_data, file_name="summary.pdf", mime="application/pdf"
            )
