from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
