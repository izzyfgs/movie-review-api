import re
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    # Ensure email is mandatory and unique
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="A user with this email already exists.")]
    )

    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        # Only these 3 fields will appear in the form
        fields = ('username', 'email', 'password')

    def validate_password(self, value):
        """Your custom password strength validation"""
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        username = self.initial_data.get('username', '')
        if value.lower() == username.lower():
            raise serializers.ValidationError("Password cannot be the same as username.")
        return value

    def create(self, validated_data):
        # Properly hash the password using create_user
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
