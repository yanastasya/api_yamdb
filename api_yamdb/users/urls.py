from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import UserViewSet, UserMeViewSet, CustomTokenObtainPairView, SignupViewSet



router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # path(
    #     'v1/users/me/',
    #     UserMeViewSet.as_view({'get': 'list', 'patch': 'update'}),
    #     name='user_me'
    # ),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupViewSet.as_view({'post': 'create'}), name='signup'),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]