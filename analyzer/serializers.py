from rest_framework import serializers
from .models import Skill, JobRole, Resource, Analysis, LoginHistory


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ('id', 'action', 'timestamp', 'ip_address')