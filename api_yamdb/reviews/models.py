from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категории (типа) произведения."""
    name = models.CharField(
        'Название категории',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
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
        'Название жанра',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
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
        'Название произведения',
        max_length=200,
    )
    year = models.IntegerField(
        'Год выпуска',
        blank=True,
        null=True,
    )
    description = models.TextField(
        'Описание',
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
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='unique_title',
            )
        ]

    def __str__(self):
        return f'«{self.name}» ({self.year}) / {self.category}'


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


class Review(models.Model):
    """Модель отзывов к произведениям."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        "Отзыв",
    )
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        "Оценка",
        validators=[
            MinValueValidator(1, 'Минимальная оценка'),
            MaxValueValidator(10, 'Максимальная оценка')
        ]
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    """Модель комментариев к отзывам."""
    author = models.ForeignKey(
        User,
        verbose_name="Автор комментария",
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        verbose_name="Отзыв",
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(
        "Текст комментария",
    )
    pub_date = models.DateTimeField(
        "Дата комментирования",
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return self.text
