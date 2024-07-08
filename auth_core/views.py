from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .serializers import UserSerializer


class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            data = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                    "user": serializer.data,
                },
            }
            return Response(data, status=status.HTTP_201_CREATED)
        elif not serializer.is_valid():

            errors = []
            for field, value in serializer.errors.items():
                if isinstance(value, list):
                    for error in value:
                        errors.append({f"{field}": field, "message": error})
                else:
                    errors.append({"field": field, "message": value})
            data = {
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400,
                "errors": errors,
            }
            return Response(data=data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        data = {
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400,
            "errors": serializer.errors,
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(email=email, password=password)
        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)

            # Construct response data
            data = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                    "user": {
                        "userId": user.userId,
                        "email": user.email,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "phone": user.phone,
                    },
                },
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
