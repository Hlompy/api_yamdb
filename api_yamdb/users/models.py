from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'US'
    MODERATOR = 'MD'
    ADMIN = 'AD'

    USER_ROLE = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    )

    role = models.CharField(
        'Пользовательская роль',
        max_length=10,
        choices=USER_ROLE,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
