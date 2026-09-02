import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher

from .skills_data import SKILL_LIST

# Load spaCy's English model once (reused every time this file is used)
nlp = spacy.load("en_core_web_sm")

# Build the PhraseMatcher once, using our skill list
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILL_LIST]
matcher.add("SKILLS", patterns)


def extract_text_from_pdf(file_path):
    """Reads a PDF file and returns all its text as one string."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_skills_from_text(text):
    """Takes resume text, finds skills from SKILL_LIST inside it."""
    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()
    for match_id, start, end in matches:
        span_text = doc[start:end].text.lower()
        for skill in SKILL_LIST:
            if skill.lower() == span_text:
                found_skills.add(skill)
                break

    return sorted(found_skills)


def extract_skills_from_resume(pdf_file_path):
    """Full pipeline: PDF file -> extracted text -> list of skills found."""
    text = extract_text_from_pdf(pdf_file_path)
    return extract_skills_from_text(text)

import re


def check_contact_info(text):
    """Checks if resume has an email and/or phone number."""
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\d{10}', text))
    return has_email, has_phone


def check_sections(text):
    """Checks if common resume sections are present."""
    text_lower = text.lower()
    sections_found = {
        "education": "education" in text_lower,
        "experience_or_projects": ("experience" in text_lower or "projects" in text_lower),
        "skills": "skills" in text_lower,
    }
    return sections_found


def check_length(text):
    """Very short resumes are usually a red flag for ATS."""
    word_count = len(text.split())
    return word_count >= 150  # a reasonable minimum for a real resume


def calculate_ats_score(text, skill_match_percentage):
    """
    Combines skill match with resume-quality checks to produce
    an overall ATS-friendliness score out of 100.
    """
    has_email, has_phone = check_contact_info(text)
    contact_score = 100 if (has_email or has_phone) else 0

    sections = check_sections(text)
    sections_score = (sum(sections.values()) / len(sections)) * 100

    length_score = 100 if check_length(text) else 40

    # Weighted final score
    ats_score = (
        skill_match_percentage * 0.60 +
        contact_score * 0.15 +
        sections_score * 0.15 +
        length_score * 0.10
    )

    return {
        "ats_score": round(ats_score, 1),
        "has_email": has_email,
        "has_phone": has_phone,
        "sections_found": sections,
        "length_ok": check_length(text),
    }