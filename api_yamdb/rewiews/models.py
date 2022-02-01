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