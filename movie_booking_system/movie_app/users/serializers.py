from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class RegisterationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    def createUser(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User Not Found!")
        
        if not check_password(password, user.password):
            raise serializers.ValidationError("Incorrect password.")
           
        return data