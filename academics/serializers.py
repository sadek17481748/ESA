"""academics/serializers.py"""
from rest_framework import serializers

from .models import ClassEnrollment, ClassGroup, YearGroup


class YearGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearGroup
        fields = ('id', 'school', 'name', 'sort_order', 'created_at')
        read_only_fields = ('id', 'school', 'created_at')


class ClassGroupSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    year_group_name = serializers.CharField(source='year_group.name', read_only=True)

    class Meta:
        model = ClassGroup
        fields = (
            'id', 'school', 'year_group', 'year_group_name', 'name',
            'teacher', 'teacher_name', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')


class ClassEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    class_name = serializers.CharField(source='class_group.name', read_only=True)

    class Meta:
        model = ClassEnrollment
        fields = ('id', 'class_group', 'class_name', 'student', 'student_name', 'enrolled_at')
        read_only_fields = ('id', 'enrolled_at')
