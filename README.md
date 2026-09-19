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
[PASTE LINK HERE]

### Login Page
[PASTE LINK HERE]

### Home Page
<img width="960" height="510" alt="Screenshot 2026-09-05 131708" src="https://github.com/user-attachments/assets/c5a7f66b-7280-4a90-9f7e-9dab61cc412e" />

### Results Page — Skill Match
<img width="960" height="510" alt="Screenshot 2026-09-05 132330" src="https://github.com/user-attachments/assets/195df1d3-c758-4b85-909e-ed8b4872cb94" />
<img width="960" height="510" alt="Screenshot 2026-09-05 132456" src="https://github.com/user-attachments/assets/0d3cf2c6-8fbd-495b-8798-8dc246ad353c" />

### Results Page — ATS Score & Charts
<img width="960" height="510" alt="Screenshot 2026-09-05 132330" src="https://github.com/user-attachments/assets/f94960b8-f90a-45ec-9877-b28566fb045f" />
[PASTE LINK HERE]

### History Page (Activity Log + Chart)
[PASTE LINK HERE]

### My Analyses Page
[PASTE LINK HERE]

### Skill-Gap API (Django REST Framework)
[PASTE LINK HERE]

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
