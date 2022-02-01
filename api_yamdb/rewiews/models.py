from django.db import models


class Category(models.Model):
    """Модель категории (типа) произведения."""
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_category',
            )
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_genre',
            )
        ]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения, к которым пишут отзывы."""
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    year = models.IntegerField(
        'Дата выхода',
        max_length=4,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'Категория',
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        'Жанр',
        Genre,
        through='GenreTitle',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи между произведением и его жанром."""
    title = models.ForeignKey(
        'Название произведения',
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        'Жанр произведения',
        Genre,
        on_delete=models.CASCADE,
    )
