from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import AmazProduct, Rank, Price, Inventory, Permission, Role, RolePermissionsPermission

class InventoryAdmin(admin.ModelAdmin):
    model = Inventory
    list_display = ['product', 'qty', 'upc', 'wh_id', 'last_modified']
    ordering = ['upc', '-qty']  # Sort by qty in descending order

admin.site.register(AmazProduct)
admin.site.register(Rank)
admin.site.register(Price)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(RolePermissionsPermission)
