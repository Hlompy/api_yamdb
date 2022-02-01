from django.db import models

from users.models import User


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


class Comment(models.Model):
    author = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.OneToOneField(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)