from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категории (типа) произведения."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
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
        verbose_name='Название',
        max_length=200,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтигн',
        default=0,
    )
    description = models.TextField(
        verbose_name='Описание',
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
    author = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    text = models.TextField()
    title =  models.OneToOneField(
        Title, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    name = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.OneToOneField(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Rating(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    review =  models.ForeignKey(
        Review,
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    sum_vote = models.PositiveIntegerField(
        default=0
    )
    count_vote = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f'Counting of votes:{self.count_vote}, Rating of votes:{self.sum_vote}'
