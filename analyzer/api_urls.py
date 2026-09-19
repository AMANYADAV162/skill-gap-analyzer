from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('skills', api_views.SkillViewSet, basename='skill')
router.register('job-roles', api_views.JobRoleViewSet, basename='jobrole')
router.register('resources', api_views.ResourceViewSet, basename='resource')
router.register('login-history', api_views.LoginHistoryViewSet, basename='login-history')
router.register('analyses', api_views.AnalysisViewSet, basename='analysis')

urlpatterns = [
    path('', include(router.urls)),
    path('skill-gap/', api_views.skill_gap_api, name='skill-gap-api'),
    path('free-courses/', api_views.free_courses_api, name='free-courses-api'),
]
