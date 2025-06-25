# Resume Format Converter 

This project allows you to upload resumes in .docx, .pdf, or .txt formats and converts them into a standardized format used by Nehish Software Solutions Pvt. Ltd.

---

## Technologies Used

- Python 3.8+
- Streamlit
- re
- python-docx
- PyPDF2

---

##  File Structure

- `streamlit_ui.py` – Streamlit frontend app
- `parsed.py` – Logic to parse resume content
- `layout.py` – Resume formatter to Nehish layout
- `samples/ouput_generated` – Contains input resumes and output
- `README.md` – This file

---

##  How to Run

1. Install dependencies:

```bash
pip install streamlit python-docx PyPDF2
```

2. Run the Streamlit app:

```bash
streamlit run streamlit_ui.py
```

3. Upload a resume and download the formatted Nehish-style .docx.

---

##  Sample Resumes

You can test the app using provided samples in the `samples/` directory:

- SatyamSinghResume.pdf
- Priya_Sharma_Academic.docx
- Aarav_Mehta_Resume.pd
- Output files: `output_*.docx`

---

##  Output Format

The formatted resume includes the following sections:

- Name (centered)
- Professional Summary
- Technical Skill Sets
- Education
- Work Experience
- Projects
- Certifications
- Achievements
- Contact

---

