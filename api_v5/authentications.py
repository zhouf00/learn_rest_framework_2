# 自定义认证类
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from . import models
# 1 继承
# 2 重新authenticate(self, request)方法，自定义认证规则
# 3 认证规则基于的条件：
#   没有认证信息返回None（游客）
#   有认证信息认证失败抛异常（非法用户）
#   有认证信息认证成功返回用户与认证信息元组（合法用户）
# 4 完全视图类的全局（settings文件中）或局部（确切的视图类）
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 前台在请求头拾认证信息，
        #   且默认规范用Authorization字段携带认证信息
        #   后台固定在请求对象的META字段中HTTP_AUTHORIZATION获取
        auth = request.META.get('HTTP_AUTHORIZATION', None)

        # 处理游客
        if auth is None:
            return None

        # 设置一下认证字段小规则（两段式）：auth 认证字符串
        auth_list = auth.split()

        # 校验合法还是非法用户
        if not (len(auth_list) == 2 and auth_list[0].lower() == 'auth'):
            raise AuthenticationFailed('认证信息，非法用户')

        # 合法的用户还需要从auth_list[1]中解析出来
        # 注： 假设一种情况：信息为abc.123.xyz，就可以解析出admin用户：实际开发，该逻辑一定是校验用户的正常逻辑
        if auth_list[1] != 'abc.123.xyz':
            raise AuthenticationFailed('用户校验失败，非法用户')

        user = models.User.objects.filter(username='admin').first()

        if not user:
            raise AuthenticationFailed('用户数据有误，非法用户')

        return (user, None)

# 登陆：帐号密码 => token（帐号密码对应的用户）
# 访问需要登录的接口： 携带token发送请求 => 校验token，得到用户