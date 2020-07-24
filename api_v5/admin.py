from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

# Register your models here.

# 自定义user表，admin后台管理
class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'mobile', 'email'),
        }),
    )

# 密码密文
admin.site.register(models.User, MyUserAdmin)
admin.site.register(models.Car)
