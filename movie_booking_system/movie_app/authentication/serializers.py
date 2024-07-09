from rest_framework import serializers
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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)