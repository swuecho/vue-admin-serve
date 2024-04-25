from django.contrib.auth.models import Group, User
from amaz_products.models import (
    Profile,
    Rank,
    Price,
    Inventory,
    Permission,
    Role,
    Parameter,
    Hardware,
    InventoryExtra,
    StandardProductAsin,
)
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from amaz_products.models import Role


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        roles = Role.objects.filter(userrolesrole__user_id=user.id)
        # token["roles"] = [r.code for r in roles]
        token["role"] = roles[0].code if roles else ""
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined", "last_login"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryGroupSerializer(serializers.Serializer):
    upc = serializers.CharField()
    product = serializers.CharField()
    total_qty = serializers.IntegerField()


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


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class HardwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = "__all__"


class InventoryExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryExtra
        fields = "__all__"


class StandardProductAsinSerilizer(serializers.ModelSerializer):
    asin = serializers.CharField(max_length=50, allow_blank=True, default="")
    comment = serializers.CharField(max_length=500, allow_blank=True, default="")

    class Meta:
        model = StandardProductAsin
        fields = "__all__"
