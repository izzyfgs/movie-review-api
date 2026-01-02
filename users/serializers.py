from django.contrib.auth.models import User
from rest_framework import serializers
<<<<<<< HEAD
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
=======

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
>>>>>>> 1e48e953e7076fcaac1d3863a58df4538ee22bba
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        
