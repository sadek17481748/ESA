"""parents/serializers.py"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ParentProfile, StudentParentLink

User = get_user_model()


class ParentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ParentProfile
        fields = ('id', 'school', 'user', 'username', 'email', 'phone', 'is_active', 'created_at')
        read_only_fields = ('id', 'school', 'created_at')


class ParentCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)


class StudentParentLinkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    parent_name = serializers.CharField(source='parent.user.username', read_only=True)

    class Meta:
        model = StudentParentLink
        fields = ('id', 'parent', 'student', 'student_name', 'parent_name', 'relationship', 'created_at')
        read_only_fields = ('id', 'created_at')
