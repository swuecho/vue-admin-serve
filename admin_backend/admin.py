# Register your models here.

from django.contrib import admin
from .models import Permission, Role, RolePermissionsPermission


admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(RolePermissionsPermission)
