from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Received registration request with data: {request.data}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"User {user.password} registered successfully")
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.error(f"Invalid registration data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie('access_token',data['access'],httponly=True,samesite='Strict')
            response.set_cookie('refresh_token',data['refresh'],httponly=True,samesite='Strict')
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token or not refresh_token:
            logger.info("No tokens found in cookies")
            return Response({"detail": "No authentication tokens provided."}, status=status.HTTP_401_UNAUTHORIZED)

        logger.info(f"Logout attempt for user with token: {access_token[:10]}...")

        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        
        # Remove the cookies
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        logger.info("Cookies removed, user logged out")
        return response