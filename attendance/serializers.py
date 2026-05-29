"""attendance/serializers.py"""
from rest_framework import serializers

from .models import AttendanceMark, AttendanceSession


class AttendanceMarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = AttendanceMark
        fields = ('id', 'session', 'student', 'student_name', 'status', 'note')


class AttendanceSessionSerializer(serializers.ModelSerializer):
    marks = AttendanceMarkSerializer(many=True, read_only=True)
    class_name = serializers.CharField(source='class_group.name', read_only=True)

    class Meta:
        model = AttendanceSession
        fields = (
            'id', 'school', 'class_group', 'class_name', 'timetable_slot',
            'session_date', 'taken_by', 'marks', 'created_at',
        )
        read_only_fields = ('id', 'school', 'taken_by', 'created_at')


class AttendanceSessionWriteSerializer(serializers.ModelSerializer):
    """Create session + bulk marks in one payload."""

    marks = AttendanceMarkSerializer(many=True, write_only=True)

    class Meta:
        model = AttendanceSession
        fields = ('class_group', 'timetable_slot', 'session_date', 'marks')
