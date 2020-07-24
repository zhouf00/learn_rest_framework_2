import re
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.response import APIResponse
from api_v5 import models

from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# 自定义jwt校验规则
from .authentications import JWTAuthentication
class UserDetail(APIView):
    permission_classes =  [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        return APIResponse(results={'username': request.user.username})



# # 必须登录后才能访问 - 通过了认证权限组件
# class UserDetail(APIView):
#     permission_classes =  [IsAuthenticated]
#     authentication_classes = [JSONWebTokenAuthentication]
#
#     def get(self, request, *args, **kwargs):
#         return APIResponse(results={'username': request.user.username})

# 实现多方式登陆签发token：帐号、手机号、邮箱等登陆
# 1 禁用认证与权限组件
# 2 拿到前台登录信息
# 3 校验得到登陆用户
# 4 签发token并返回
from . import serializers
class LoginAPIView(APIView):
    # 禁用认证与权限组件
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 拿到前台登录信息，交给序列化类，规则：帐号用usr传，密码用pwd传
        user_ser = serializers.UserModelSerializer(data=request.data)
        # 序列化类校验得到登录用户与token存放在序列化对象中
        user_ser.is_valid(raise_exception=True)
        # 取出登录用户与token返回给前台
        return APIResponse(
            data_msg='post ok',
            token=user_ser.token,
            results=serializers.UserModelSerializer(user_ser.user).data
        )
    # 无封闭思想的逻辑
    def my_post(self, request, *args, **kwargs):
        usr = request.data.get('usr')
        pwd = request.data.get('pwd')

        if re.match(r'.+@.+', usr):
            user_query = models.User.objects.filter(email=usr)
        elif re.match(r'1[3-9][0-9]{9}',usr):
            user_query = models.User.objects.filter(mobile=usr)
        else:
            user_query = models.User.objects.filter(username=usr)
        user_obj = user_query.first()
        if user_obj and user_obj.check_password(pwd):
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            return APIResponse(results={'username': user_obj.username}, token=token)
        return APIResponse(data_msg='不可控错误')


# Car的群查接口
from rest_framework.generics import ListAPIView
# 1 drf的searchFilter - 搜索过滤
from rest_framework.filters import SearchFilter

# 2 drf的OrderingFilter - 排序过滤
from rest_framework.filters import OrderingFilter

# 3 drf的分布类 - 自定义
from . import pagenations

# 自定义过滤器
from .filters import LimitFilter, CarFilterSet

from django_filters.rest_framework import DjangoFilterBackend
class CarListAPIView(ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer

    # 局部配置 过滤类们（全局配置用DEFAULT_FILETER_BACKENDS）
    filter_backends = [SearchFilter, OrderingFilter, LimitFilter, DjangoFilterBackend]

    # SearchFilter过滤类依赖的过滤条件 => 接口： /cars/?search=...
    search_fields = ['name', 'price']
    # eg: /cars/?search=1, name和price中包含1的数据都会被查询出

    # OrderingFilter过滤类依赖的条件 => 接口： /cars/?ordering=...
    ordering_fields = ['pk', 'price']
    # eg：/cars/?ordering=-price, pk, 先按price降序，如果出现price相同，再按pk升序

    # 分页组件 - 给视图类配置分页类即可 -分页类需要自定义，继承drf提供的
    # pagination_class = pagenations.MyPageNumberPagination
    # pagination_class = pagenations.MyLimitOffsetPagination

    # 需要排序条件的辅助
    # pagination_class = pagenations.MyCursorPagination

    filter_class = CarFilterSet
