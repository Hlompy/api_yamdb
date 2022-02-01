from django.db import models


class Category(models.Model):
    """Модель категории (типа) произведения."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
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
    """Модель категории жанра."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
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
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        max_length=4,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
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
        Title,
        verbose_name='Название произведения',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр произведения',
        on_delete=models.CASCADE,
    )
