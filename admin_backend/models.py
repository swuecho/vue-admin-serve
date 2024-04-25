from django.db import models
from django.conf import settings


## frontend Permission
class Permission(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    parent_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    path = models.CharField(max_length=255, null=True)
    redirect = models.CharField(max_length=255, null=True)
    icon = models.CharField(max_length=50, null=True)
    component = models.CharField(max_length=255, null=True)
    layout = models.CharField(max_length=50, null=True, blank=True)
    keep_alive = models.IntegerField(null=True)
    method = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    show = models.BooleanField()
    enable = models.BooleanField()
    order = models.IntegerField(blank=True, null=True)


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.TextField(null=True)
    nick_name = models.CharField(max_length=50, null=True)


"""
>>> r1 = Role.objects.get(id=1)
>>> r1
<Role: SUPER_ADMIN>
>>> r1.
r1.DoesNotExist(                   r1.delete(                         r1.objects                         r1.serializable_value(
r1.MultipleObjectsReturned(        r1.enable                          r1.pk                              r1.unique_error_message(
r1.check(                          r1.from_db(                        r1.prepare_database_save(          r1.userrolesrole_set(
r1.clean(                          r1.full_clean(                     r1.refresh_from_db(                r1.validate_unique(
r1.clean_fields(                   r1.get_deferred_fields(            r1.rolepermissionspermission_set(  
r1.code                            r1.id                              r1.save(                           
r1.date_error_message(             r1.name                            r1.save_base(         
"""


class Role(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RolePermissionsPermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("role", "permission"),)

    def __str__(self):
        return self.role.name + " - " + self.permission.name


"""
>>> user_role1.
user_role1.DoesNotExist(             user_role1.full_clean(               user_role1.role_id
user_role1.MultipleObjectsReturned(  user_role1.get_deferred_fields(      user_role1.save(
user_role1.check(                    user_role1.id                        user_role1.save_base(
user_role1.clean(                    user_role1.objects                   user_role1.serializable_value(
user_role1.clean_fields(             user_role1.pk                        user_role1.unique_error_message(
user_role1.date_error_message(       user_role1.prepare_database_save(    user_role1.user
user_role1.delete(                   user_role1.refresh_from_db(          user_role1.user_id
user_role1.from_db(                  user_role1.role                      user_role1.validate_unique(
>>> user_role1.role
<Role: SUPER_ADMIN>
>>> user_role1.user
<User: firelectronix@gmail.com>
>>> user_role1.user_id
3
>>> user_role1.user_id
3
"""


class UserRolesRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
