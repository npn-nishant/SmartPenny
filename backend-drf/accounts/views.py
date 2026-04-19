from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({
                "success": True,
                "message": "Account created successfully",
                "data": {
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "role": user.role,   # ✅ added role
                },
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not phone or not password:
            return Response({
                "success": False,
                "message": "Phone and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, phone=phone, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)

            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "role": user.role,
                },
                "tokens": tokens
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)