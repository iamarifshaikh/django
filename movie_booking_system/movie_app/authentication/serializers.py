from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        logger.info(f"Creating user with data: {validated_data}")
        try:
            user = User(
                name=validated_data['name'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            logger.info(f"Password set for user {user.name}")
            user.save()
            logger.info(f"User {user.name} saved successfully")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
        raise serializers.ValidationError("Invalid Credentials")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)