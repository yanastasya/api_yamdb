from django.db import models
import datetime as dt
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Жанры"    


class Categories(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"    


class Titles(models.Model):
    """Произведения, к которым пишут отзывы.
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(
        verbose_name="название произведения",
        max_length=200,
    )
    category = models.ForeignKey(
        Categories,
        verbose_name="Категория",        
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,        
        verbose_name="Жанр",               
        through='TitlesGenre',
    )
    year = models.IntegerField(
        verbose_name="год создания произведения",
    )
    description = models.TextField(
        verbose_name="описание произведения",
    )

    def __str__(self):
        return self.name

    """Нельзя добавлять произведения, которые еще не вышли
    (год выпуска не может быть больше текущего).
    """
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(year__lte=dt.datetime.today().year),
                name='year__lte=now_year'
            )
        ],
        verbose_name_plural = "Произведения"


class TitlesGenre(models.Model):
    """Модель для связи произведений и жанров."""
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.titles} {self.genre}'
