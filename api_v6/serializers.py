import re
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from api_v5 import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# 1 前台提交多种登陆信息都采用一个key，所以后台可以自定义反序列化字段进行对应
# 2 序列化类要处理序列化与反序列化，要在fields中设置model绑定的Model类所有使用到的字段
# 3 区分序列化字段与反序列化字段read_only | write_only
# 4 在自定义校验规则中（局部钩子、全局钩子）校验数据是否合法、确定登录的用户、根据用户签发token
# 5 将登录的用户与签发的token保存在序列化类对象中
class UserModelSerializer(serializers.ModelSerializer):
    # 自定义反序列字段：一定要设置write_only，只能与反序列化，不会与model类字段映射
    usr = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['usr', 'pwd', 'username', 'mobile', 'email']
        # 系统校验规则
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'mobile': {
                'read_only': True
            },
            'email': {
                'read_only': True
            },
        }

    def validate(self, attrs):
        # 多方式登陆：各分支处理得到该方式对应的用户
        usr = attrs.get('usr')
        pwd = attrs.get('pwd')
        if re.match(r'.+@.+', usr):
            user_query = models.User.objects.filter(email=usr)
        elif re.match(r'1[3-9][0-9]{9}',usr):
            user_query = models.User.objects.filter(mobile=usr)
        else:
            user_query = models.User.objects.filter(username=usr)
        user_obj = user_query.first()
        if user_obj and user_obj.check_password(pwd):
            # 签发token，将token存放到，实例化类对象中
            payload = jwt_payload_handler(user_obj)
            self.token = jwt_encode_handler(payload)
            # 将当前用户与签发的token都保存在序列化对象中
            self.user = user_obj
            return attrs

        raise serializers.ValidationError({'data': '数据有误'})


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Car
        fields = ['name', 'price', 'brand']

