# Resume Format Converter  

This project allows you to upload resumes in `.docx`, `.pdf`, or `.txt` formats and converts them into the **standardized Nehish format**.

# Technologies Used  
- Python 3.8+  
- Streamlit  
- python-docx  
- PyPDF2  
- pytesseract + pdf2image (for OCR)  
- FPDF  

# File Structure  
- `streamlit_ui.py` – Streamlit frontend  
- `parsed.py` – Resume parsing logic  
- `layout.py` – Nehish-style formatting  
- `samples/` – Sample input resumes and outputs  
- `README.md` – Project info  

## How to Run  
1. Install dependencies:  
   pip install -r requirements.txt  
2. Start the app:  
   streamlit run streamlit_ui.py  
3. Upload a resume and download the formatted `.docx`.  

# Output Format  
The generated resume includes:  
- Name  
- Professional Summary  
- Skills  
- Work Experience  
- Projects  
- Certifications  
- Achievements  
- Education  
