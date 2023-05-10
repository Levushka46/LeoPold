from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'friends', views.FriendViewSet, basename='friends')
router.register(r'friend_requests', views.FriendRequestViewSet, basename='friend_requests')

urlpatterns = [
    path("", views.index, name="index"),
    path("", include(router.urls)),
]