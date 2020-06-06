from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^test/$', views.TestView.as_view()),
    url(r'^test1/$', views.TestAuthenticatedAPIView.as_view()),
    url(r'^test2/$', views.TestAuthenticatedOrReadOnlyAPIView.as_view()),
    url(r'^test3/$', views.TestAdminOrReadOnlyAPIView.as_view()),
    url(r'^sms/$', views.TestSMSAPIView.as_view())
]