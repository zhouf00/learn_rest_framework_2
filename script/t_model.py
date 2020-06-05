# Django脚本化启动
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_rest_framework_2.settings')
django.setup()

from api_v5 import models

user = models.User.objects.first()
print(user.username)
# print(user.groups.first().name)

from django.contrib.auth.models import Group

group = Group.objects.first()
print(group.name)
print(group.user_set.first().username)
print(group.permissions.first().name)

from django.contrib.auth.models import Permission
p_16 = Permission.objects.filter(pk=22).first()
print('p16',p_16.user_set.first().username)
p_17 = Permission.objects.filter(pk=22).first()
print(p_17.group_set.first().name)