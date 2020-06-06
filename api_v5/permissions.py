from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class MyPermission(BasePermission):

    def has_permission(self, request, view):

        # return bool(
        #     request.method in SAFE_METHODS or
        #     request.user and
        #     request.user.is_authenticated
        # )
        r1 = request.method in SAFE_METHODS
        group = Group.objects.filter(name='管理员').first()
        groups = request.user.groups.all()
        r2 = group and groups
        r3 = group in groups
        return r1 or r2 and r3