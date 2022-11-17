from django.db import models

"""+ модель юзера."""


class Genre(models.Model):
    """Категории жанров."""
    pass


class Categorie(models.Model):
    """Категории произведений."""
    pass


class Title(models.Model):
    """Произведения, к которым пишут отзывы.
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(
        verbose_name="название произведения",
        max_length=200,
    )
    category = models.ForeignKey(
        Categorie,
        verbose_name="Категория",        
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,        
        verbose_name="Жанр",
        related_name='titles',               
        through='TitleGenre',
        null=True,
        blank=True,
    )
    year = models.IntegerField(
        verbose_name="год создания произведения",
    )
    description = models.TextField(
        verbose_name="описание произведения",
    )

    def __str__(self):
        return self.name
    

class Rewiew(models.Model):
    """Отзывы к произведениям."""
    pass


class Comment(models.Model):
    """Комментарии к отзывам."""
    pass
