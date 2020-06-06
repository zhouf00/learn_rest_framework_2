from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet, ViewSet
from utils.response import APIResponse

class TestView(APIView):

    def get(self, request, *args, **kwargs):
        # 如何通过了认证组件，reuqest.user就一定有值
        # 游客：AnonymousUser
        # 用户：User表中的具体用户对象
        print(request.user)
        return APIResponse(0, 'test get ok')


# 只有登录的用记才能访问
from rest_framework.permissions import IsAuthenticated
class TestAuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return APIResponse(0, 'test1 登录才能访问的接口 ok')

# 游客只读，登陆无限制
from rest_framework.permissions import IsAuthenticatedOrReadOnly
class TestAuthenticatedOrReadOnlyAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return APIResponse(0, 'test2 游客只读的接口 ok')

    def post(self, request, *args, **kwargs):
        return APIResponse(0, 'test2 写 ok')


# 游客只读，登录用户只读，只有登录用户属于 管理员 分组，才可以增删改
from .permissions import MyPermission
class TestAdminOrReadOnlyAPIView(APIView):
    permission_classes = [MyPermission]

    def get(self, request, *args, **kwargs):
        return APIResponse(0, 'test3 游客只读的接口 ok')

    def post(self, request, *args, **kwargs):
        return APIResponse(0, 'test3 写 ok')


from .throttles import SMSRateThrottle
class TestSMSAPIView(APIView):
    throttle_classes = [SMSRateThrottle]
    def get(self, request, *args, **kwargs):
        return APIResponse(0, 'get 获取验证码 ok')

    def post(self, request, *args, **kwargs):
        return APIResponse(0, 'POST 写 ok')

