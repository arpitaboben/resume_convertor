import streamlit as st
from parsed import parse_resume, save_uploaded_file
from layout import generate_docx
import os
import pythoncom
from docx import Document
from fpdf import FPDF

pythoncom.CoInitialize()

st.set_page_config(page_title="Resume Format Converter", layout="centered")
st.title(" Resume Format Converter")

uploaded_file = st.file_uploader("Upload your resume (.pdf, .docx, .txt):", type=["pdf", "docx", "txt"])

def clean_text_for_pdf(text):
    # Replace common unicode dashes and quotes with ASCII equivalents
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201c': '"',  # left double quote
        '\u201d': '"',  # right double quote
        '\u2022': '*',  # bullet
        # Add more as needed
    }
    for uni, ascii_char in replacements.items():
        text = text.replace(uni, ascii_char)
    # Remove any other non-latin-1 characters
    return text.encode('latin-1', errors='ignore').decode('latin-1')

def docx_to_pdf(docx_path, pdf_path):
    doc = Document(docx_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for para in doc.paragraphs:
        clean_para = clean_text_for_pdf(para.text)
        pdf.multi_cell(0, 10, clean_para)
    pdf.output(pdf_path)

def convert_to_pdf(input_path, ext):
    output_pdf = input_path.rsplit('.', 1)[0] + ".pdf"
    if ext == ".docx":
        try:
            docx_to_pdf(input_path, output_pdf)
            return output_pdf
        except Exception as e:
            st.error(f"docx2pdf conversion failed: {e}")
            return input_path
    elif ext == ".txt":
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            with open(input_path, "r", encoding="utf-8") as f:
                for line in f:
                    pdf.cell(0, 10, txt=line.strip(), ln=True)
            pdf.output(output_pdf)
            return output_pdf
        except Exception as e:
            st.error(f"FPDF conversion failed: {e}")
            return input_path
    return input_path

if uploaded_file:
    with st.spinner(" Parsing resume..."):
        saved_path = save_uploaded_file(uploaded_file)
        ext = os.path.splitext(saved_path)[1].lower()
        # Remove conversion for .docx files
        pdf_path = saved_path
        if ext == ".pdf":
            pdf_path = saved_path
        elif ext == ".txt":
            pdf_path = convert_to_pdf(saved_path, ext)
        # For .docx, pass directly
        parsed_data = parse_resume(pdf_path)

        if parsed_data:
            st.success("Resume parsed successfully!")
            with st.expander("Preview Extracted Data"):
                st.json(parsed_data)
            docx_path = generate_docx(parsed_data)
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="Download Formatted Resume",
                    data=f,
                    file_name="nehish_format_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.error(" Failed to parse resume. Try another file.")
