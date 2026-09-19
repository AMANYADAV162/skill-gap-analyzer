import os
from .forms import ResumeUploadForm, SignupForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import LoginHistory
from .signals import get_client_ip
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage


from .models import Resource, Analysis
from .resume_parser import extract_skills_from_resume, extract_text_from_file, calculate_ats_score

@login_required
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

    # ---- ATS Score calculation ----
    resume_text = extract_text_from_file(file_path)
    ats_result = calculate_ats_score(resume_text, match_percentage)

    # ---- Step 6: Get free resources for each missing skill ----
    missing_skill_resources = []
    for skill_name in missing_skills:
        resources = Resource.objects.filter(skill__name=skill_name)
        missing_skill_resources.append({"skill": skill_name, "resources": resources})

    # ---- Step 7: Save this analysis to the database (for "My Analyses" history) ----
    Analysis.objects.create(
        user=request.user,
        job_role=job_role,
        resume_file=uploaded_file,
        matched_skills=", ".join(matched_skills),
        missing_skills=", ".join(missing_skills),
        match_percentage=match_percentage,
    )

    context = {
        "job_role": job_role,
        "matched_skills": matched_skills,
        "missing_skill_resources": missing_skill_resources,
        "match_percentage": match_percentage,
        "ats_result": ats_result,
    }
    return render(request, "analyzer/results.html", context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            LoginHistory.objects.create(
                user=user,
                action='signup',
                ip_address=get_client_ip(request),
            )
            login(request, user)
            send_mail(
                subject="Welcome to Skill Gap Analyzer!",
                message=f"Hi {user.username},\n\nThanks for signing up. Upload your resume and find out exactly what skills stand between you and your dream role.\n\n— Skill Gap Analyzer Team",
                from_email=None,
                recipient_list=[user.email] if user.email else [],
                fail_silently=False,
            )
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def history_view(request):
    history = LoginHistory.objects.filter(user=request.user)
    action_counts = {
        'signup': history.filter(action='signup').count(),
        'login': history.filter(action='login').count(),
        'logout': history.filter(action='logout').count(),
    }
    return render(request, 'analyzer/history.html', {
        'history': history,
        'action_counts': action_counts,
    })
@login_required
def my_analyses_view(request):
    analyses = Analysis.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'analyzer/my_analyses.html', {'analyses': analyses})