# 🎯 AI-Based Skill Gap Analyzer

A Django web application that analyzes resumes using NLP to identify skill gaps for a target job role, calculates an ATS (Applicant Tracking System) compatibility score, and recommends free learning resources — including live YouTube course search — to close the gap. Includes full user authentication, account activity tracking, and a REST API.

---

## 📖 Overview

Students and job-seekers often don't know exactly which skills they're missing for a specific role — and even when they do, they don't know where to start learning. This tool automates that analysis:

1. Create an account and log in
2. Upload your resume (PDF or DOCX)
3. Select a target job role
4. Get an instant skill-match percentage, an ATS compatibility score, curated + live free course recommendations for every missing skill, and a saved history of every analysis you've run

---

## ✨ Features

- **User Authentication** — Signup, login, and logout with a modern, professional SaaS-style UI
- **Account Activity History** — Every signup/login/logout event is automatically logged (action, timestamp, IP address) and visualized with a chart
- **Resume Parsing (NLP)** — Extracts skills from PDF **and DOCX** resumes using spaCy's `PhraseMatcher`, matched against a master skill list
- **Skill Gap Analysis** — Compares extracted skills against a job role's required skills and calculates a match percentage
- **ATS Compatibility Score** — Rule-based scoring that checks skill match, contact info, resume sections (Education/Experience/Skills), and resume length, visualized with a gauge chart
- **Learning Resource Recommendations** — Curated free resources for every missing skill, plus a **live "Find free courses" search** powered by the YouTube Data API v3
- **My Analyses** — Every resume analysis is saved so users can review their past results (job role, match %, date, resume file) at any time
- **REST API (Django REST Framework)** — Skills, Job Roles, Resources, Analyses, and Login History are all exposed via a browsable REST API, including a dedicated skill-gap analysis endpoint
- **Email Notifications** — Automated welcome email sent on signup (SMTP)
- **Admin Panel** — Manage job roles, skills, and resources without touching code
- **Custom UI** — A distinctive "skill journey" progress visual, interactive Chart.js visualizations, and a modern two-column signup page

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| API | Django REST Framework |
| Database | MySQL |
| NLP | spaCy (`PhraseMatcher`) |
| Document Parsing | pdfplumber (PDF), python-docx (DOCX) |
| External API | YouTube Data API v3 |
| Email | Django SMTP backend |
| Frontend | HTML, CSS (custom design system), JavaScript, Chart.js, Django Templates |

---

## 🗄️ Database Design

- **Skill** — master list of skills
- **JobRole** — target roles, linked to Skills via a Many-to-Many relationship
- **Resource** — free learning resources, linked to a Skill via a One-to-Many relationship
- **Analysis** — stores each resume analysis event (job role, resume file, matched/missing skills, match %, timestamp)
- **LoginHistory** — stores each signup/login/logout event per user (action, timestamp, IP address)

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
```

### Configure settings

In `skillgap/settings.py`, set your **MySQL** database (`DATABASES` section) and your **email** credentials for signup notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-gmail-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

YOUTUBE_API_KEY = 'your-youtube-data-api-key'
```

> ⚠️ For a real deployment, move `SECRET_KEY`, the database password, `EMAIL_HOST_PASSWORD`, and `YOUTUBE_API_KEY` into environment variables instead of hardcoding them, and add your `.env`/settings overrides to `.gitignore`.

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create an admin account
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to use the app, and `http://127.0.0.1:8000/admin/` to manage job roles, skills, and resources.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/skills/` | GET | List all skills |
| `/api/job-roles/` | GET | List all job roles with required skills |
| `/api/resources/` | GET | List learning resources |
| `/api/login-history/` | GET | Logged-in user's account activity history |
| `/api/analyses/` | GET | Saved resume analyses |
| `/api/skill-gap/` | POST | Upload resume + job role → match %, ATS score, matched/missing skills |
| `/api/free-courses/` | GET | Live free YouTube course search for a given skill |

---

## 📸 Screenshots

### Signup Page
<img width="960" height="510" alt="Screenshot 2026-09-20 133203" src="https://github.com/user-attachments/assets/73a12a4a-9376-4406-94f8-d1132fc7998a" />

### Login Page
<img width="960" height="510" alt="Screenshot 2026-09-20 132550" src="https://github.com/user-attachments/assets/d47851e9-b0d8-424a-9b0b-a308e1e6c741" />


### Home Page
<img width="960" height="510" alt="Screenshot 2026-09-20 133409" src="https://github.com/user-attachments/assets/6deaa0b6-8fdc-426e-b011-ea63fafd91d3" />


### Results Page — Skill Match & ATS Score Charts
<img width="960" height="510" alt="Screenshot 2026-09-20 133513" src="https://github.com/user-attachments/assets/d001bced-033d-4401-934b-aa7db0b84f74" />
<img width="960" height="510" alt="Screenshot 2026-09-20 133556" src="https://github.com/user-attachments/assets/9dad977d-4b4c-4d60-be9e-800cdb5e3ef8" />


### History Page (Activity Log + Chart)
<img width="960" height="510" alt="Screenshot 2026-09-20 134407" src="https://github.com/user-attachments/assets/d7253b2d-bc4a-442c-8ddd-4b885e9f85cb" />
<img width="960" height="510" alt="Screenshot 2026-09-20 134429" src="https://github.com/user-attachments/assets/852878ce-9184-4053-ac43-c6bfd17cc6c4" />


### My Analyses Page
<img width="960" height="510" alt="Screenshot 2026-09-20 134348" src="https://github.com/user-attachments/assets/14edf9c7-e687-4bce-9c91-48b092dae552" />

### Admin Panel
<img width="1920" height="1080" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/86319cf3-27c2-4fc4-8a6a-a271d1f8e255" />

---

## 🔮 Future Scope

- Personalized skill recommendations based on a user's analysis history
- Multi-language resume support
- Employer/recruiter-facing bulk resume screening mode
- Mobile app powered by the existing REST API
- More job roles and an expanded skill database
- Advanced resume quality checks (action verbs, quantifiable achievements)
- Deployment on a cloud platform

---

## 👤 Author

**Aman Yadav**
BCA, Department of Computer Applications, DR. VSIPS
