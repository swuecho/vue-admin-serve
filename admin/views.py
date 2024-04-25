from django.http import Http404
from admin.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {"code": 0, "message": "OK", "data": serializer.validated_data},
            status=status.HTTP_200_OK,
        )


class SwitchRoleView(APIView):
    def post(self, request, *args, **kwargs):
        user_and_token = JWTAuthentication().authenticate(request)
        role = request.data["role"]

        if user_and_token is None:
            return Http404  # better
        user = user_and_token[0]

        token = RefreshToken.for_user(user)
        # Add custom claims
        token["role"] = role

        data = {}
        data["refresh"] = str(token)
        data["access"] = str(token.access_token)

        update_last_login(None, user)
        print(data)
        return Response(
            {"code": 0, "message": "OK", "data": data},
            status=status.HTTP_200_OK,
        )