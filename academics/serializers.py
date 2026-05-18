"""academics/serializers.py"""
from rest_framework import serializers

from .models import ClassGroup


class ClassGroupSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)

    class Meta:
        model = ClassGroup
        fields = (
            'id', 'school', 'name', 'year_group', 'teacher', 'teacher_name', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')
