from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin_backend.models import Permission, Profile, Role
from admin_backend.util import role_permissions
from django.core.serializers import serialize


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        roles = Role.objects.filter(userrolesrole__user_id=user.id)
        # token["roles"] = [r.code for r in roles]
        token["role"] = roles[0].code if roles else ""
        token["permissions"] = [
            p["code"] for p in role_permissions(token["role"])
        ] 
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined", "last_login"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
