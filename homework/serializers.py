"""homework/serializers.py"""
from rest_framework import serializers

from .models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Assignment
        fields = (
            'id', 'school', 'class_group', 'class_group_name', 'subject', 'subject_name',
            'teacher', 'title', 'description', 'assignment_type', 'due_date', 'created_at',
        )
        read_only_fields = ('id', 'school', 'teacher', 'created_at')


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Submission
        fields = (
            'id', 'assignment', 'assignment_title', 'student', 'student_name', 'body',
            'submitted_at', 'status', 'teacher_note', 'signed_off_by', 'signed_off_at', 'created_at',
        )
        read_only_fields = ('id', 'signed_off_by', 'signed_off_at', 'created_at')
