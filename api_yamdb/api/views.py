from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Categorie
from .serializers import GenreSerializer, CategorieSerializer
from .serializers import TitleGetSerializer, TitlePostSerializer
from users.permissions import IsRoleAdminOrSuperUser
from users.pagination import Pagination


class CategorieViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Эндпоинт  api/v1/categories/.
    GET запрос: Получение списка всех категорий.
    Права доступа: Доступно без токена. Поиск по названию категории.
    POST запрос: Создать категорию. Права доступа: Администратор.
    Поле slug каждой категории должно быть уникальным.
    DEL запрос на api/v1/genres/slug/ удаляет админ.
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    #permission_classes = IsRoleAdminOrSuperUser


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Эндпоинт  api/v1/genres/.
    GET запрос: Получение списка всех жанров.
    Права доступа: Доступно без токена. Поиск по названию жанра.
    POST запрос: Создать жанр. Права доступа: Администратор.
    Поле slug каждого жанра должно быть уникальным.
    DEL запрос на api/v1/genres/slug/ удаляет админ.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """"Эндпоинт api/v1/titles/.
    GET: Получить список всех объектов.+ Права доступа: Доступно без токена.
    фильтры по genre__slug  и category__slug, name и year.
    POST:Добавить новое произведение. Права доступа: Администратор.
    Нельзя добавлять произведения, которые еще не вышли.
    При добавлении нового произведения требуется указать уже существующие
    category и genre.
    Эндпоинт api/v1/titles/id:
    GET: получение инфы об объекте. genre кортежем, category как объект.
    Доступно любому пользователю.
    PATCH: получение инфы о произведении по id.
    Доступно только администратору.
    DEL: удаление произведения по id - только администратор.
    """
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer

        return TitlePostSerializer


