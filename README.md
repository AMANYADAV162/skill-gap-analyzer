# 🎯 AI-Based Skill Gap Analyzer

A Django web application that analyzes resumes using NLP to identify skill gaps for a target job role, calculates an ATS (Applicant Tracking System) compatibility score, and recommends free learning resources to close the gap.

---

## 📖 Overview

Students and job-seekers often don't know exactly which skills they're missing for a specific role — and even when they do, they don't know where to start learning. This tool automates that analysis:

1. Upload your resume (PDF)
2. Select a target job role
3. Get an instant skill-match percentage, an ATS compatibility score, and curated free resources for every missing skill

---

## ✨ Features

- **Resume Parsing (NLP)** — Extracts skills from PDF resumes using spaCy's `PhraseMatcher`, matched against a master skill list
- **Skill Gap Analysis** — Compares extracted skills against a job role's required skills and calculates a match percentage
- **ATS Compatibility Score** — Rule-based scoring that checks skill match, contact info, resume sections (Education/Experience/Skills), and resume length
- **Learning Resource Recommendations** — Free video and article resources (freeCodeCamp, W3Schools, etc.) for every missing skill
- **Admin Panel** — Manage job roles, skills, and resources without touching code
- **Custom UI** — A distinctive "skill journey" progress visual instead of a generic progress bar

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | MySQL |
| NLP | spaCy (`PhraseMatcher`) |
| PDF Parsing | pdfplumber |
| Frontend | HTML, CSS (custom design system), Django Templates |

---

## 🗄️ Database Design

Four core models:

- **Skill** — master list of skills
- **JobRole** — target roles, linked to Skills via a Many-to-Many relationship
- **Resource** — free learning resources, linked to a Skill via a One-to-Many relationship
- **Analysis** — stores each resume analysis event (job role, matched/missing skills, match %)

---

## 🚀 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/AMANYADAV162/skill-gap-analyzer.git
cd skill-gap-analyzer

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure your MySQL database in skillgap/settings.py (DATABASES section)

# Run migrations
python manage.py migrate

# Create an admin account
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to use the app, and `http://127.0.0.1:8000/admin/` to manage job roles, skills, and resources.

---

## 📸 Screenshots

### Home Page
*(add screenshot here)*

### Results Page — Skill Match
*(add screenshot here)*

### Results Page — ATS Score
*(add screenshot here)*

### Admin Panel
<img width="1920" height="1080" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/86319cf3-27c2-4fc4-8a6a-a271d1f8e255" />


---

## 🔮 Future Scope

- User authentication with analysis history tracking
- More job roles and an expanded skill database
- Advanced resume quality checks (action verbs, quantifiable achievements)
- Deployment on a cloud platform

---

## 👤 Author

**Aman Yadav**
BCA, Department of Computer Applications, DR. VSIPS
