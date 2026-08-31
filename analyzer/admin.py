from django.contrib import admin
from .models import Skill, JobRole, Resource, Analysis


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    filter_horizontal = ("required_skills",)


admin.site.register(Skill)
admin.site.register(Resource)
admin.site.register(Analysis)