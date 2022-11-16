from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import UserViewSet, UserMeViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'v1/users/me/',
        UserMeViewSet.as_view({'get': 'list', 'patch': 'update'})
    ),
    path('v1/', include(router.urls)),
]
