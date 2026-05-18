from rest_framework import serializers

from .models import TeacherProfile


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = (
            'id', 'school', 'user', 'username', 'subject',
            'employee_code', 'is_active', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')
