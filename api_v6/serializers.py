import re
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from api_v5 import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(serializers.ModelSerializer):
    # 自定义反序列字段
    usr = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['usr', 'pwd', 'username', 'mobile', 'email']
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

    def validate_usr(self, value):
        print(value)
        return value

    def validate_pwd(self, value):
        print(value)
        return value

    def validate(self, attrs):
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