from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reviews.models import Title, Genre, Categorie, Review
from .serializers import GenreSerializer, CategorieSerializer
from .serializers import TitleGetSerializer, TitlePostSerializer
from .serializers import CommentSerializer, ReviewSerializer
from .filters import TitleFilter
from api.permissions import IsAdmimOrReadOnly, IsAdmimOrModeratorOrReadOnly


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
    lookup_field = 'slug'
    permission_classes = [IsAdmimOrReadOnly]


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdmimOrReadOnly]


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdmimOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer

        return TitlePostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Эндпоинт /api/v1/titles/{title_id}/reviews/{review_id}/comments/.
    GET запрос: Получить список всех комментариев к отзыву по id.
    Права доступа: Доступно без токена.
    POST запрос: Добавить новый комментарий для отзыва.
    Права доступа: Аутентифицированные пользователи.
    Эндпоинт /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/.
    GET запрос: Получить комментарий для отзыва по id.
    Права доступа: Доступно без токена.
    PATCH и DEL запросы: частичное изменение или удаление комментария по id.
    Права доступа: Автор отзыва, модератор или администратор.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAdmimOrModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Эндпоинт /api/v1/titles/{title_id}/reviews/.
    GET запрос: получение списка всех отзывов. Доступно без токена.
    POST запрос: добавить новый отзыв. Пользователь может оставить
    только один отзыв на произведение.
    Права доступа: Аутентифицированные пользователи.
    Эндпоинт /api/v1/titles/{title_id}/reviews/{review_id}/.
    GET запрос: Получить отзыв по id для указанного произведения.
    Права доступа: Доступно без токена.
    PATCH и DEL запросы: частичное изменение или удаление отзыва по id.
    Права доступа: Автор отзыва, модератор или администратор.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAdmimOrModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not Review.objects.filter(
            author=self.request.user, title=self.kwargs.get('title_id')
        ).exists():
        #if request.data.is_valid:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {'message': 'Вы оставляли отзыв на это творение.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
