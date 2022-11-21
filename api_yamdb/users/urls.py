from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import UserViewSet, UserMeViewSet, CustomTokenObtainPairView, SignupViewSet



v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        r'v1/users/me/',
        UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'update'}),
        name='user_me'
    ),
    path(r'v1/', include(v1_router.urls)),
    path(r'v1/auth/signup/', SignupViewSet.as_view({'post': 'create'}), name='signup'),
    path(r'v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]