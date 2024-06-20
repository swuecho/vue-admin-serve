from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from admin_backend.app_permission import IsSuperAdmin
from admin_backend.models import (
    Permission,
    Profile,
    Role,
    RolePermissionsPermission,
    UserRolesRole,
)
from admin_backend.serializers import (
    GroupSerializer,
    PermissionSerializer,
    ProfileSerializer,
    RoleSerializer,
    UserSerializer,
)


def get_claims_from_request(request):
    token = request.headers.get("Authorization")
    if token:
        token = AccessToken(token.split(" ")[1])
        return token.payload
    return {}


@permission_classes([IsSuperAdmin])
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request):
        users = User.objects.all().order_by("id")
        data_list = []
        for user in users:
            # user_roles = UserRolesRole.objects.filter(user=user)
            # role_ids = [user_role.role_id for user_role in user_roles]
            # roles = Role.objects.filter(id__in=role_ids)
            # r1.userrolesrole_set.all()
            roles = Role.objects.filter(userrolesrole__user_id=user.id)
            data_list.append(
                {
                    **UserSerializer(user).data,
                    "roles": RoleSerializer(roles, many=True).data,
                }
            )
        return Response(data={"results": data_list})


@permission_classes([IsSuperAdmin])
class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    filterset_fields = ["enable", "name"]
    permission_classes = [IsSuperAdmin]

    def list(self, request: Request):
        roles = Role.objects.all().order_by("name")
        data = []
        for role in roles:
            permission_ids = [
                p["permission_id"]
                for p in RolePermissionsPermission.objects.filter(role=role.id).values(
                    "permission_id"
                )
            ]
            data.append({**RoleSerializer(role).data, "permission_ids": permission_ids})
        return Response(data={"results": data})

    def perform_update(self, serilizer):
        payload = self.request.data
        serilizer.save()
        if payload["permission_ids"]:
            RolePermissionsPermission.objects.filter(role_id=payload["id"]).delete()
            for permission_id in payload["permission_ids"]:
                RolePermissionsPermission(
                    role_id=payload["id"], permission_id=permission_id
                ).save()
        return Response(data={"results": self.request.data})


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Permission.objects.all().order_by("id")
    serializer_class = PermissionSerializer
    filterset_fields = ["enable", "name"]
    permission_classes = [IsSuperAdmin]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RolePermissionTree(APIView):
    def get(self, request):
        """based on user role and permission to get list"""
        roles = Role.objects.filter(userrolesrole__user_id=request.user.id)
        jwt_claims = get_claims_from_request(request)
        current_role_code = jwt_claims.get("role")
        user_permission_ids = RolePermissionsPermission.objects.filter(
            role_id__in=[r.id for r in roles if r.code == current_role_code]
        )
        permission_id_set = {d.permission.id for d in user_permission_ids}
        top_level_permissions = Permission.objects.filter(
            parent_id__isnull=True, id__in=permission_id_set
        )
        data = []
        for permission in sorted(
            top_level_permissions, key=lambda x: x.order if x.order else 0
        ):
            children = sorted(
                permission.children.all(), key=lambda x: x.order if x.order else 0
            )
            data.append(
                {
                    **PermissionSerializer(permission).data,
                    "children": PermissionSerializer(
                        [child for child in children if child.id in permission_id_set],
                        many=True,
                    ).data,
                }
            )
        full_resp = {"code": 0, "message": "OK", "data": data}
        return Response(data=full_resp)


@permission_classes([IsSuperAdmin])
class RolePermissionMenuTree(APIView):
    """MENU only"""

    def get(self, request):
        # Get all top-level permissions
        data = []
        top_level_permissions = Permission.objects.filter(
            parent_id__isnull=True, type__exact="MENU"
        )
        for permission in sorted(
            top_level_permissions, key=lambda x: x.order if x.order else 0
        ):
            children = sorted(
                permission.children.filter(type__exact="MENU"),
                key=lambda x: x.order if x.order else 0,
            )
            data.append(
                {
                    **PermissionSerializer(permission).data,
                    "children": PermissionSerializer(children, many=True).data,
                }
            )
        full_resp = {"code": 0, "message": "OK", "data": data}
        return Response(data=full_resp)


class RolePermissionMenuValidate(APIView):
    """MENU only"""

    def get(self, request):
        # Get all top-level permissions
        path = request.query_params["path"]
        exists = Permission.objects.filter(
            type__exact="MENU", path__exact=path
        ).exists()

        full_resp = {"code": 0, "message": "OK", "data": exists}
        return Response(data=full_resp)


@permission_classes([IsSuperAdmin])
class RolePermissionBaseTree(APIView):
    def get(self, request):
        # Get all top-level permissions
        data = []
        top_level_permissions = Permission.objects.filter(parent_id__isnull=True)
        for permission in sorted(
            top_level_permissions, key=lambda x: x.order if x.order else 0
        ):
            children = sorted(
                permission.children.all(), key=lambda x: x.order if x.order else 0
            )
            data.append(
                {
                    **PermissionSerializer(permission).data,
                    "children": PermissionSerializer(children, many=True).data,
                }
            )
        full_resp = {"code": 0, "message": "OK", "data": data}
        return Response(data=full_resp)


class UserDetail(APIView):
    def get(self, request):
        user = request.user
        user_roles = UserRolesRole.objects.filter(user=user)
        role_ids = [user_role.role_id for user_role in user_roles]
        roles = Role.objects.filter(id__in=role_ids, enable=True)
        roles_list = RoleSerializer(roles, many=True).data
        jwt_claims = get_claims_from_request(request)
        role_code = jwt_claims.get("role")

        current_role = roles_list[0] if roles_list else {}

        if role_code:
            for role_data in roles_list:
                if role_data["code"] == role_code:
                    current_role = role_data
                    break
        data = {
            **UserSerializer(user).data,
            "roles": roles_list,
            "profile": ProfileSerializer(
                Profile.objects.filter(user_id=user.id).first()
            ).data,
            "current_role": current_role,
        }
        return Response(data={"code": 0, "message": "OK", "data": data})


## create or update
@api_view(["GET", "POST"])
@permission_classes([IsSuperAdmin])
def user_roles_create_or_update(request):
    payload = request.data
    user_id = payload["id"]
    role_ids = payload["role_ids"]
    UserRolesRole.objects.filter(user=user_id).delete()
    for role_id in role_ids:
        UserRolesRole(role_id=role_id, user_id=user_id).save()
    return Response(data=True)


@api_view(["GET", "POST"])
@permission_classes([IsSuperAdmin])
def role_users_create_or_update(request):
    payload = request.data
    role_id = payload["id"]
    user_ids = payload["user_ids"]
    for u_id in user_ids:
        if not UserRolesRole.objects.filter(role_id=role_id, user_id=u_id).count():
            UserRolesRole(role_id=role_id, user_id=u_id).save()
    return Response(data=True)


# api/roles/switch?role=OPERATOR
# http://localhost:3200/api/auth/current-role/switch/OPERATOR


@api_view(["POST"])
def logout(request):
    """logout, alway return true"""
    payload = request.data
    user = request.user
    print(payload)
    print(user)
    return Response(data=True)
