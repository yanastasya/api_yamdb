from django.db import models

"""+ модель юзера."""


class Genre(models.Model):
    """Категории жанров."""
    pass


class Categories(models.Model):
    """Категории произведений."""
    pass


class Titles(models.Model):
    """Произведения, к которым пишут отзывы.
    Определённый фильм, книга или песенка."""
    pass


class Rewiews(models.Model):
    """Отзывы к произведениям."""
    pass


class Comments(models.Model):
    """Комментарии к отзывам."""
    pass
