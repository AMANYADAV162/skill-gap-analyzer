from django.db import models


# ---------- Table 1: Skill ----------
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------- Table 2: JobRole ----------
class JobRole(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(Skill, related_name="job_roles")

    def __str__(self):
        return self.title


# ---------- Table 3: Resource ----------
class Resource(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, default="youtube")

    def __str__(self):
        return f"{self.skill.name} - {self.title}"


# ---------- Table 4: Analysis ----------
class Analysis(models.Model):
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to="resumes/")
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    match_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.job_role.title} ({self.match_percentage}%)"