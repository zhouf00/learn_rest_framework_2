import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework import exceptions

class JWTAuthentication(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')

        # 自定义校验规则: auth token jwt
        token = self.parse_jwt_token(jwt_token)

        if token is None:
            return None

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('token已过期')
        except:
            raise exceptions.AuthenticationFailed('非法用户')

        user = self.authenticate_credentials(payload)

        return (user, token)

    # 自定义校验规则: auth token jwt，auth为前言，jwt为后言
    def parse_jwt_token(self, jwt_token):
        tokens = jwt_token.split()
        print(tokens)
        if len(tokens) != 3 or tokens[0].lower() != 'auth' or tokens[2].lower() != 'jwt':
            return None
        return tokens[1]