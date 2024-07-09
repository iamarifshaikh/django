from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import User
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
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

class LoginView(TokenObtainPairView):
    def post(self,request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            response.set_cookie('access_token', access_token,httponly=True, samesite='Strict')
            response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Strict')
        return Response
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        response = Response({"message":"Logged Out Successfully"},status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh-token")
        return response