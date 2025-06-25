import streamlit as st
from parsed import parse_resume
from layout import generate_nehish_docx
import tempfile
import os

st.set_page_config(page_title="Nehish Resume Format Converter")
st.title("📄 Resume Format Converter")

st.write("Upload a resume (PDF, DOCX, or TXT) and download the formatted version in Nehish style.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    # Extract structured data
    st.info("Parsing the resume...")
    parsed_data = parse_resume(temp_path)

    if parsed_data:
        st.success("Resume parsed successfully!")

        # Generate formatted DOCX
        st.info("Generating formatted resume...")
        formatted_docx_path = generate_nehish_docx(parsed_data)

        with open(formatted_docx_path, "rb") as file:
            st.download_button(
                label="📥 Download Formatted Resume",
                data=file,
                file_name="nehish_formatted_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.error("Failed to parse the resume. Please check the file content.")
