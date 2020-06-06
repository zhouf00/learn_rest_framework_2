from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    url(r'^jlogin/$', obtain_jwt_token),
    url(r'user/detail/$', views.UserDetail.as_view()),

    url(r'login/$', views.LoginAPIView.as_view()),
]