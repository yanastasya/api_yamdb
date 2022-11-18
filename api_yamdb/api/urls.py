from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategorieViewSet, TitleViewSet

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategorieViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
