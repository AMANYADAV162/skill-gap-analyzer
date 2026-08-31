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