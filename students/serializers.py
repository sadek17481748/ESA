"""
students/serializers.py
API representation of StudentProfile.
"""
from rest_framework import serializers

from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = (
            'id', 'school', 'school_name', 'user', 'first_name', 'last_name',
            'year_group', 'admission_number', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')
