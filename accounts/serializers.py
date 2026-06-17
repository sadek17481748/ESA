"""
accounts/serializers.py
Serializes User for API responses and handles registration validation.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Safe user fields for /me and list endpoints — no password hash."""

    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'school', 'school_name',
        )
        read_only_fields = ('id', 'role', 'school')


class RegisterSerializer(serializers.ModelSerializer):
    """Creates a user; enforces school FK except for super_admin."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'role', 'school')

    def validate(self, attrs):
        role = attrs.get('role', 'student')
        school = attrs.get('school')
        if role != 'super_admin' and not school:
            raise serializers.ValidationError(
                {'school': 'School is required for this role.'},
            )
        if role == 'super_admin' and school:
            raise serializers.ValidationError(
                {'school': 'Super admin must not belong to a school.'},
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
