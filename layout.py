from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import tempfile

def add_heading(doc, title):
    p = doc.add_paragraph()
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(13)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

def add_content(doc, content):
    if isinstance(content, list):
        for item in content:
            if item.strip():
                doc.add_paragraph(item.strip(), style="List Bullet")
    elif isinstance(content, str) and content.strip():
        doc.add_paragraph(content.strip())

def generate_nehish_docx(data):
    doc = Document()

    # Header
    name = data.get("name", "").strip() or "Name"
    doc.add_paragraph(name).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    first_name = name.split()[0] if name else "Name"
    doc.add_paragraph(first_name).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    if data.get("summary"):
        doc.add_paragraph("\nP r o f e s s i o n a l   S u m m a r y", style='Heading 2')
        add_content(doc, data["summary"])

    if data.get("skills"):
        doc.add_paragraph("\nT e c h n i c a l   S k i l l   S e t s", style='Heading 2')
        add_content(doc, data["skills"])

    if data.get("education"):
        doc.add_paragraph("\nE d u c a t i o n", style='Heading 2')
        add_content(doc, data["education"])

    if data.get("experience"):
        doc.add_paragraph("\nW o r k   E x p e r i e n c e", style='Heading 2')
        add_content(doc, data["experience"])

    if data.get("projects"):
        doc.add_paragraph("\nP r o j e c t s", style='Heading 2')
        add_content(doc, data["projects"])

    if data.get("certifications"):
        doc.add_paragraph("\nC e r t i f i c a t i o n s", style='Heading 2')
        add_content(doc, data["certifications"])

    if data.get("achievements"):
        doc.add_paragraph("\nA c h i e v e m e n t s", style='Heading 2')
        add_content(doc, data["achievements"])

    if data.get("contact"):
        doc.add_paragraph("\nC o n t a c t", style='Heading 2')
        add_content(doc, f"info: {data['contact'][0]}")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name
