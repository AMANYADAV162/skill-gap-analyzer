from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobRole


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ResumeUploadForm(forms.Form):
    job_role = forms.ModelChoiceField(
        queryset=JobRole.objects.all(),
        label="Select Target Job Role",
        empty_label="-- Choose a Job Role --",
    )
    resume_file = forms.FileField(
        label="Upload Your Resume (PDF or DOCX)",
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf,.docx"}),
    )

    def clean_resume_file(self):
        file = self.cleaned_data["resume_file"]
        name = file.name.lower()
        if not (name.endswith(".pdf") or name.endswith(".docx")):
            raise forms.ValidationError("Please upload a PDF or DOCX file only.")
        return file