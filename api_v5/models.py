from django.db import models

# Create your models here.
# 基本用户权限访问控制的认证 - RBAC - Role-Based Access Control
# 自己了解：基于auth认证规则

# Django框架采用的是RBAC认证规则，RBAC谁规则通常会会为三表规则、五表规则，Django采用的是六表规则

# 三表： 用户表、角色表、权限表
# 五表： 用户表、角色表、权限表、用户角色关系表、角色权限关系表
# 六表： 用户表、角色表、权限表、用户角色关系表、角色权限关系表、用户权限关系表


# 用户表：角色groups，权限user_permissions
# 角色表：用户user_set，权限permissions
# 权限表：用户user_set, 角色group_set

# 重点：如果自定义User表后，再另一个项目中采用原生User表，完成数据表，可能失败
# 1 卸载Django重新
# 2 将Django.contrib下面的admin、auth下的数据库迁移记录文件清空
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'api_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Car(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name='车名')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    brand = models.CharField(max_length=16, verbose_name='品牌')


    class Meta:
        db_table = 'api_car'
        verbose_name = '汽车表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name