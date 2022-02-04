from django.urls import include, path
from rest_framework import routers

from users.views import UserSignupViewSet, UsersViewSet, creating_token

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'users',
    UsersViewSet,
    basename='users'
)
router_v1.register('auth/signup', UserSignupViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/', creating_token, name='creating_token')
]
