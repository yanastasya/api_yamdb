from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet

app_name = 'api'

 

v1_router = DefaultRouter() 

#v1_router.register('titles', TitlesViewSet)
#v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoriesViewSet)
 

urlpatterns = [
    path('v1/', include(v1_router.urls)),
] 