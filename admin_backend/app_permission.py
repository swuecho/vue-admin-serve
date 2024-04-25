from rest_framework.permissions import BasePermission
from admin_backend.models import Role, UserRolesRole


class IsSuperAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    role = "SUPER_ADMIN"

    def has_permission(self, request, view):
        role_super_admin = Role.objects.filter(code__exact="SUPER_ADMIN").first()
        has_super_admin_role = (
            UserRolesRole.objects.filter(
                user_id=request.user.id, role=role_super_admin
            ).count()
            > 0
        )
        return bool(request.user and has_super_admin_role)
