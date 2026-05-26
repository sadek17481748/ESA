"""subjects/serializers.py"""
from rest_framework import serializers

from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    lead_teacher_name = serializers.CharField(source='lead_teacher.user.username', read_only=True)

    class Meta:
        model = Subject
        fields = (
            'id', 'school', 'name', 'track', 'code', 'lead_teacher', 'lead_teacher_name',
            'is_active', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')

