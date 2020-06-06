from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.response import APIResponse


# 必须登录后才能访问 - 通过了认证权限组件
class UserDetail(APIView):
    permission_classes =  [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, *args, **kwargs):
        return APIResponse(results={'username': request.user.username})

# 实现多方式登陆签发token：帐号、手机号、邮箱等登陆
# 1 禁用认证与权限组件
# 2 拿到前台登录信息
# 3 校验得到登陆用户
# 4 签发token并返回
from . import serializers
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_ser = serializers.UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        print(user_ser.token)
        return APIResponse(
            data_msg='post ok',
            token=user_ser.token,
            results=serializers.UserModelSerializer(user_ser.user).data
        )
