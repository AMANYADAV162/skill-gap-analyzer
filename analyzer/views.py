import os
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .forms import ResumeUploadForm
from .models import Resource
from .resume_parser import extract_skills_from_resume


def home(request):
    """Shows the upload form."""
    form = ResumeUploadForm()
    return render(request, "analyzer/home.html", {"form": form})


def analyze_resume(request):
    """Handles the uploaded resume: extract skills, compare, show result."""
    if request.method != "POST":
        return render(request, "analyzer/home.html", {"form": ResumeUploadForm()})

    form = ResumeUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, "analyzer/home.html", {"form": form})

    job_role = form.cleaned_data["job_role"]
    uploaded_file = form.cleaned_data["resume_file"]

    # ---- Step 1: Save the uploaded PDF temporarily ----
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "resumes"))
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_path = fs.path(filename)

    # ---- Step 2: Extract skills from the resume using NLP ----
    resume_skills = extract_skills_from_resume(file_path)
    resume_skills_set = set(resume_skills)

    # ---- Step 3: Get skills required for the chosen job role ----
    required_skills_set = set(s.name for s in job_role.required_skills.all())

    # ---- Step 4: Compare ----
    resume_skills_lower = {s.lower() for s in resume_skills_set}
    required_skills_lower = {s.lower(): s for s in required_skills_set}

    matched_skills = sorted(v for k, v in required_skills_lower.items() if k in resume_skills_lower)
    missing_skills = sorted(v for k, v in required_skills_lower.items() if k not in resume_skills_lower)
    # ---- Step 5: Calculate match percentage ----
    if required_skills_set:
        match_percentage = round((len(matched_skills) / len(required_skills_set)) * 100, 1)
    else:
        match_percentage = 0.0

    # ---- Step 6: Get free resources for each missing skill ----
    missing_skill_resources = []
    for skill_name in missing_skills:
        resources = Resource.objects.filter(skill__name=skill_name)
        missing_skill_resources.append({"skill": skill_name, "resources": resources})

    context = {
        "job_role": job_role,
        "matched_skills": matched_skills,
        "missing_skill_resources": missing_skill_resources,
        "match_percentage": match_percentage,
    }
    return render(request, "analyzer/results.html", context)