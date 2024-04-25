"""bestqa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from admin_backend.views import MyTokenObtainPairView, SwitchRoleView

from .ninja import api as ninja_api
from django.urls import include, path
from rest_framework import routers

from admin_backend import views
from admin_backend import views_api
from admin_backend import views_user_role_permission
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r"users", views_user_role_permission.UserViewSet)
router.register(r"roles", views_user_role_permission.RoleViewSet)
router.register(r"permissions", views_user_role_permission.PermissionViewSet)
router.register(r"profiles", views_user_role_permission.ProfileViewSet)
# router.register(r"inventory_group", views.InventoryGroupList)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


# Define a regular expression pattern to split the UPC at non-word characters
# Perform aggregation based on the first split part of the UPC code
# formatted_upc = Func(
#     F('upc'),
#     Value(","),
#     function='regexp_split_to_array', output=ArrayField(TextField())
# )

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/role/permissions/tree/",
        views_user_role_permission.RolePermissionTree.as_view(),
        name="role_permission_tree",
    ),
    path(
        "api/permissions/base/tree/",
        views_user_role_permission.RolePermissionBaseTree.as_view(),
        name="role_permission_tree",
    ),
    path(
        "api/permissions/menu/tree/",
        views_user_role_permission.RolePermissionMenuTree.as_view(),
        name="role_permission_tree",
    ),
    path(
        "api/permission/menu/validate",
        views_user_role_permission.RolePermissionMenuValidate.as_view(),
        name="permission_menu_validate",
    ),
    path(
        "api/permissions/button/<int:parent_id>/",
        views_api.permissions_button_list,
        name="button list",
    ),
    path(
        "api/user/detail",
        views_user_role_permission.UserDetail.as_view(),
        name="user_detail",
    ),
    path(
        "api/user/roles/",
        views_user_role_permission.user_roles_create_or_update,
        name="user_detail",
    ),
    path(
        "api/role/users/",
        views_user_role_permission.role_users_create_or_update,
        name="user_detail",
    ),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("ninja/", TokenAuthMiddleware(ninja_api.urls)),
    path("ninja/", ninja_api.urls),
    # currently not used, but can be used.
    path("api/auth/switch_role/", SwitchRoleView.as_view(), name="switch-role"),
    path("api/auth/login", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    #      {
    #     "code": 0,
    #     "message": "OK",
    #     "data": true,
    #     "originUrl": "/auth/logout"
    # }
    # path("api/auth/logout", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_fresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT )
# urlpatterns = [re_path(r"^dj/", include(admin_urlpatterns))]
