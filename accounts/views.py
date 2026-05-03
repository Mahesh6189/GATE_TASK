from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return Response({"error": "Username already exists"}, status=400)

        return Response({"message": "User created", "user": user.username})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Fields required"}, status=400)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Login success",
                "user_id": user.id,
                "username": user.username,
                "token": token.key   # 🔥 THIS IS REQUIRED
            })

        return Response({"message": "Invalid credentials"}, status=400)