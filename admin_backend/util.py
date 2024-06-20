from admin_backend.app_permission import IsSuperAdmin
from admin_backend.models import Permission, Role, RolePermissionsPermission


def role_permissions(current_role_code):
    if current_role_code == IsSuperAdmin.role:
        permissions = Permission.objects.all().order_by("order").values("name", "code")
    else:
        user_role_id = Role.objects.filter(code=current_role_code)
        user_permissions = RolePermissionsPermission.objects.filter(
            role_id__in=[r.id for r in user_role_id]
        )
        permission_ids = {permission.permission_id for permission in user_permissions}
        permissions = (
            Permission.objects.filter(id__in=permission_ids)
            .order_by("order")
            .values("name", "code")
        )

    return permissions
