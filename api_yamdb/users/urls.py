from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import include, path

from .views import UserViewSet, UserMeViewSet, CustomTokenObtainPairView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'v1/users/me/',
        UserMeViewSet.as_view({'get': 'list', 'patch': 'update'})
    ),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
