import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterationSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Configure logging
logger = logging.getLogger(__name__)

class RegisterationView(APIView):
    def post(self,request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.createUser(serializer.validated_data)
            logger.info(f"User  registered successfully: {user.email}")
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Registeration failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self,request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
             # Extract validated email and password from serializer
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            logger.info(f"Attempting to authenticate user: {email}")

            
            if user is not None:
                login(request,user)
                refresh = RefreshToken.for_user(user)
                logger.info(f"User logged in: {user.email}")
                return Response({ "message": "Login successful.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                logger.error("Login failed: Invalid credentials")
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED) 
        
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)