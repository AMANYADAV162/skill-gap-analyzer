from django import forms
from .models import JobRole


class ResumeUploadForm(forms.Form):
    job_role = forms.ModelChoiceField(
        queryset=JobRole.objects.all(),
        label="Select Target Job Role",
        empty_label="-- Choose a Job Role --",
    )
    resume_file = forms.FileField(label="Upload Your Resume (PDF only)")

    def clean_resume_file(self):
        file = self.cleaned_data["resume_file"]
        if not file.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Please upload a PDF file only.")
        return file