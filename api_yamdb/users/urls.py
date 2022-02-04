from django.urls import include, path
from rest_framework import routers

from users.views import UserJSWTokenViewSet, UserSignupViewSet, UsersViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'users',
    UsersViewSet,
    basename='users'
)
router_v1.register('auth/signup', UserSignupViewSet)
router_v1.register('auth/token', UserJSWTokenViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
