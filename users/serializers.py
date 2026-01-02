import re
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # 1. Explicitly define email to force it to show in the API form
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            # 2. Add extra validation to ensure email is mandatory
            'email': {'required': True, 'allow_blank': False}
        }

    def validate_email(self, value):
        """Check if the email is already in use."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        # ... keep your existing password validation logic here ...
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        # Use self.initial_data safely
        username = self.initial_data.get('username', '')
        if value.lower() == username.lower():
            raise serializers.ValidationError("Password cannot be the same as username.")
        return value

    def create(self, validated_data):
        # Use create_user to ensure password hashing is handled correctly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        
