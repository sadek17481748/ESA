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

    def validate(self, attrs):
        track = attrs.get('track', getattr(self.instance, 'track', None))
        lead = attrs.get('lead_teacher', getattr(self.instance, 'lead_teacher', None))
        if track in (Subject.TRACK_HIFZ, Subject.TRACK_ALIMIYAH) and not lead:
            raise serializers.ValidationError(
                {'lead_teacher': 'Hifz and Alimiyah subjects need a lead teacher assigned.'}
            )
        return attrs


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — saved Hifz track without requiring lead_teacher
# ---------------------------------------------------------------------------
# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = '__all__'
