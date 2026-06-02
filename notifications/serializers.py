"""notifications/serializers.py"""
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'school', 'notification_type', 'title', 'message',
            'link_path', 'is_read', 'created_at',
        )
        read_only_fields = ('id', 'school', 'created_at')
