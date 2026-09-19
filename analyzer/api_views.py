from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
 
from .models import Skill, JobRole, Resource, Analysis, LoginHistory
from .serializers import (
    SkillSerializer, JobRoleSerializer, ResourceSerializer,
    AnalysisSerializer, LoginHistorySerializer,
)
from .resume_parser import (
    extract_text_from_pdf,
    extract_skills_from_text,
    calculate_ats_score,
)
 
 
# ---------------------------------------------------------------------------
# Read-only browse endpoints
# ---------------------------------------------------------------------------
 
class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
 
 
class JobRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer
    permission_classes = [permissions.AllowAny]
 
 
class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.AllowAny]
 
 
class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)
 
 
class AnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    # Analysis model mein 'user' field nahi hai, isliye per-user filter
    # nahi laga sakte — sabhi analyses list hongi.
    queryset = Analysis.objects.all().order_by('-created_at')
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
 
 
# ---------------------------------------------------------------------------
# Skill gap analysis endpoint
# ---------------------------------------------------------------------------
 
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def skill_gap_api(request):
    """
    POST /api/skill-gap/
    multipart/form-data:
        resume   = <pdf file>
        job_role = <JobRole id>
    """
    resume_file = request.FILES.get('resume')
    job_role_id = request.data.get('job_role')
 
    if not resume_file or not job_role_id:
        return Response(
            {'error': 'resume file and job_role are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )
 
    try:
        job_role = JobRole.objects.get(id=job_role_id)
    except JobRole.DoesNotExist:
        return Response({'error': 'Invalid job_role id'}, status=status.HTTP_404_NOT_FOUND)
 
    required_skill_names = set(job_role.required_skills.values_list('name', flat=True))
 
    try:
        resume_text = extract_text_from_pdf(resume_file)
    except Exception:
        return Response(
            {'error': 'Could not read the uploaded PDF'},
            status=status.HTTP_400_BAD_REQUEST,
        )
 
    # extract_text_from_pdf() ne file pointer end tak padh liya hai,
    # Analysis.objects.create() mein save karne se pehle usse rewind karna hoga
    resume_file.seek(0)
 
    extracted_skills = set(extract_skills_from_text(resume_text))
 
    matched = required_skill_names & extracted_skills
    missing = required_skill_names - extracted_skills
    match_percentage = (
        round(len(matched) / len(required_skill_names) * 100, 2)
        if required_skill_names else 0
    )
 
    ats_info = calculate_ats_score(resume_text, match_percentage)
 
    Analysis.objects.create(
        job_role=job_role,
        resume_file=resume_file,
        matched_skills=", ".join(sorted(matched)),
        missing_skills=", ".join(sorted(missing)),
        match_percentage=match_percentage,
    )
 
    return Response({
        'job_role': job_role.title,
        'matched_skills': sorted(matched),
        'missing_skills': sorted(missing),
        'match_percentage': match_percentage,
        'ats_score': ats_info['ats_score'],
        'has_email': ats_info['has_email'],
        'has_phone': ats_info['has_phone'],
        'sections_found': ats_info['sections_found'],
    })
 
# ---------------------------------------------------------------------------
# Live free courses (YouTube) for a given skill
# ---------------------------------------------------------------------------
from .youtube_api import fetch_free_courses


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def free_courses_api(request):
    """
    GET /api/free-courses/?skill=Python
    Returns live free YouTube course/tutorial results for the given skill.
    """
    skill_name = request.query_params.get('skill')
    if not skill_name:
        return Response({'error': 'skill query param is required'}, status=status.HTTP_400_BAD_REQUEST)

    courses = fetch_free_courses(skill_name)
    return Response({'skill': skill_name, 'courses': courses})