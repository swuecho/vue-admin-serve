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



    
