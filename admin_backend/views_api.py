from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from admin_backend.app_permission import IsSuperAdmin
from admin_backend.models import Permission
from admin_backend.serializers import PermissionSerializer


@api_view()
@permission_classes([IsSuperAdmin])
def permissions_button_list(request: Request, parent_id: int):
    button_permissions = Permission.objects.filter(
        parent_id=parent_id, type__exact="BUTTON"
    ).order_by("id")
    data = [PermissionSerializer(p).data for p in button_permissions]
    return Response({"results": data})
