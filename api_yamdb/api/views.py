from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404 


from reviews.models import Titles, Genre, Categories
from .serializers import CategoriesSerializer


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Эндпоинт  api/v1/categories/
    GET запрос: Получение списка всех категорий (GET запрос к api/v1/categories).
    Права доступа: Доступно без токена. Поиск по названию категории.    
    POST запрос: Создать категорию. Права доступа: Администратор.
    Поле slug каждой категории должно быть уникальным.
    """ 

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    search_fields = ('name')
    pagination_class = LimitOffsetPagination
    #permission_classes = (IsAdminOrReadOnly,) нужен кастомный перм

    