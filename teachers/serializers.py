"""teachers/serializers.py"""
from rest_framework import serializers

from .models import TeacherProfile


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = (
            'id', 'school', 'user', 'username', 'email', 'subject',
            'employee_code', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')


class TeacherCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    subject = serializers.CharField(max_length=120, required=False, allow_blank=True)
    employee_code = serializers.CharField(max_length=40, required=False, allow_blank=True)
