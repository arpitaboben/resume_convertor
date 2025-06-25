from PyPDF2 import PdfReader
from docx import Document as DocxDoc
import re

def parse_resume(file_path):
    resume = {
        "name": "",
        "contact": [],
        "summary": [],
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "achievements": []
    }

    lines = []

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.splitlines())

    elif file_path.endswith(".docx"):
        doc = DocxDoc(file_path)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text and text not in lines:
                        lines.append(text)

        for para in doc.paragraphs:
            text = para.text.strip()
            if text and text not in lines:
                lines.append(text)

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    lines = [l.strip() for l in lines if l.strip()]
    lines = [l for l in lines if not any(x in l.lower() for x in ["enhancv", "powered by", "www."])]

   
    section_keywords = ["skills", "education", "experience", "project", "certification", "achievement", "contact"]
    skill_keywords = [
        "python", "tensorflow", "keras", "flask", "nlp", "git", "api", "openai", "gemini", "sql",
        "tableau", "machine learning", "backend", "frontend", "opencv", "sqlalchemy", "github", "react",
        "excel", "power", "bi", "communication", "microsoft", "editing", "creativity"
    ]

    name_assigned = False
    summary_done = False

    for i, line in enumerate(lines):
        lower = line.lower()

        if not name_assigned and i < 10 and line.replace(" ", "").isalpha():
            if len(line.strip()) >= 5 and len(line.split()) <= 4:
                resume["name"] = line.strip()
                name_assigned = True
                continue

        if not resume["name"]:
            words = line.strip().split()
            if len(words) in [2, 3] and all(w[0].isupper() for w in words if w.isalpha()):
                resume["name"] = line.strip()

        if any(x in lower for x in ["linkedin","@", "gmail","+91", "contact", "phone", "mobile", "number", "call","address", "city", "state", "country"]):
            resume["contact"].append(line)
            continue

        if not summary_done:
            summary_done = True
        elif len(resume["summary"]) <1 and "summary" not in lower:
            if resume["name"] not in line:            
                if line.lower()in["sum m ary","summary"]:
                    resume["summary"] = []     
                else:
                    resume["summary"].append(line)
                    continue

        if lower in ["education", "certifications", "projects and certifications"]:
            continue
        keywords = ["creative", "communication", "editing", "sql", "tableau", "power bi", "excel",
            "flask", "nlp", "openai", "gemini", "tensorflow", "keras", "git", "api","python",# Programming Languages
    "Python", "Java", "C", "C++", "JavaScript", "TypeScript", "SQL", "R", "Go", "Ruby", "Kotlin", "Swift", "Bash",
    
    # Web Development
    "HTML", "CSS", "Bootstrap", "React.js", "Angular", "Vue.js", "jQuery",
    "Node.js", "Express.js", "Django", "Flask", "Next.js"
    
    # Data Science & ML/AI
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
    "OpenCV", "NLP", "Computer Vision", "Deep Learning", "Reinforcement Learning", "Hugging Face",
    
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase", "Oracle", "Redis", "Cassandra",
    
    # DevOps & Tools
    "Git", "GitHub", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Ansible", "Terraform",
    
    # Cloud Platforms
    "AWS", "Azure", "Google Cloud Platform", "Firebase", "Heroku", "Netlify", "Vercel",
    
    # Data Visualization & BI
    "Power BI", "Tableau", "Excel", "Matplotlib", "Seaborn", "Plotly", "Looker Studio",
    
    # Testing & QA
    "Selenium", "JUnit", "TestNG", "Postman", "Cypress", "PyTest",
    
    # Cybersecurity
    "Wireshark", "Nmap", "Burp Suite", "Kali Linux", "Ethical Hacking", "Firewalls", "IDS", "IPS",
    
    # Mobile Development
    "Android Studio", "Flutter", "React Native", "Swift", "Xcode",
    
    # APIs & Integration
    "REST API", "GraphQL", "JSON", "XML", "WebSockets", "OAuth", "Stripe API",
    "Google Maps API", "OpenAI API", "Gemini API"
]

        if any(k in lower for k in keywords):
            matched = [k for k in keywords if k in lower]
            resume["skills"].extend(matched)
            continue
  
        if any(k in lower for k in ["certificate", "coursera", "udemy", "bootcamp", "openai", "microsoft", "ibm", "module"]):
            resume["certifications"].append(line)
            continue
        
        if any(k in lower for k in ["finalist", "award", "leader", "selected", "winner","achieved", "honor", "recognition", "top performer"]):
            resume["achievements"].append(line)
            continue

        if any(k in lower for k in [ "built", "flask app","website","app","web app", "serenitybot", "todo list", "ai system"]):
            resume["projects"].append(line)
            continue

        if any(k in lower for k in ["intern", "experience", "developer", "worked", "company", "organization"]):
            resume["experience"].append(line)
            continue

        if any(k in lower for k in ["university", "b.tech", "education", "academic", "college", "school", "gpa", "cgpa"]):
            resume["education"].append(line)
            continue

        if any(k in lower for k in skill_keywords):
            tokens = re.split(r"[\u2022\-,:;/| ]+", line)
            for token in tokens:
                clean = token.strip().lower()
                if clean in skill_keywords:
                    resume["skills"].append(clean)
            continue

    for key in resume:
        if isinstance(resume[key], list):
            resume[key] = list(dict.fromkeys(resume[key]))

    return resume