from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze/", views.analyze_resume, name="analyze_resume"),
    path("test-skill-gap/", TemplateView.as_view(template_name="analyzer/skillgap_test.html"), name="test-skill-gap"),
    path("history/", views.history_view, name="history"),
        path("my-analyses/", views.my_analyses_view, name="my-analyses"),
]