from django.urls import include, path
from rest_framework import routers

from users.views import UsersViewSet, creating_token, signup

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', creating_token, name='creating_token')
]
