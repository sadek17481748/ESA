"""timetable/serializers.py"""
from rest_framework import serializers

from .models import TimetableSlot


class TimetableSlotSerializer(serializers.ModelSerializer):
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)

    class Meta:
        model = TimetableSlot
        fields = (
            'id', 'school', 'class_group', 'class_group_name', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'weekday', 'weekday_display',
            'start_time', 'end_time', 'room', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')
