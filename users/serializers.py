from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    # 1. Email is required and must be unique in the database
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # 2. Password will show as an input but won't be displayed in the API response
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        style={'input_type': 'password'} # This makes it a masked password field in the browser
    )

    class Meta:
        model = User
        # 3. Only these 3 fields will appear in your browser endpoint
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # 4. Use create_user to ensure the password is encrypted/hashed properly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
