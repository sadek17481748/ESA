"""
schools/serializers.py
JSON shape for School in the REST API.
"""
from rest_framework import serializers

from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id', 'name', 'contact_email', 'subscription_tier',
            'status', 'stripe_account_id', 'created_at',
        )
        read_only_fields = ('id', 'created_at', 'stripe_account_id')
