from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'is_staff')

class RegisterReceptionistSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {'input_type': 'password'}
            },
            'role': {'read_only': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format")
            
        if self.instance is None:
            if CustomUser.objects.filter(email__iexact=value).exists():
                raise serializers.ValidationError("A user with this email already exists")
        return value.lower()

    def validate(self, data):
        """Validate password matching and complexity"""
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise serializers.ValidationError({
                'password': "Passwords do not match"
            })

        # Basic password complexity requirements
        if password:
            if not any(char.isupper() for char in password):
                raise serializers.ValidationError({
                    'password': "Password must contain at least one uppercase letter"
                })
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError({
                    'password': "Password must contain at least one number"
                })

        return data

    def create(self, validated_data):
        """Create a new receptionist user"""
        validated_data.pop('password_confirmation')
        try:
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', '').strip(),
                last_name=validated_data.get('last_name', '').strip(),
                role='receptionist'
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")

class RegisterManagerSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {'input_type': 'password'}
            },
            'role': {'read_only': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format")
            
        if self.instance is None:
            if CustomUser.objects.filter(email__iexact=value).exists():
                raise serializers.ValidationError("A user with this email already exists")
        return value.lower()

    def validate(self, data):
        """Validate password matching and complexity"""
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise serializers.ValidationError({
                'password': "Passwords do not match"
            })

        return data

    def create(self, validated_data):
        """Create a new manager user"""
        validated_data.pop('password_confirmation')
        try:
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', '').strip(),
                last_name=validated_data.get('last_name', '').strip(),
                role='manager'
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        """Validate login credentials"""
        email = data.get('email').lower()
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'non_field_errors': ["Email and password are required"]
            })

        user = authenticate(email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError({
                'non_field_errors': ["Unable to log in with provided credentials"]
            })
            
        if not user.is_active:
            raise serializers.ValidationError({
                'non_field_errors': ["This account is inactive"]
            })

        return {
            'user': user,
            'email': email
        }