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
    (определённый фильм, книга или песенка).
    """
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        related_name='titles',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)


class Rewiews(models.Model):
    """Отзывы к произведениям."""
    pass


class Comments(models.Model):
    """Комментарии к отзывам."""
    pass
