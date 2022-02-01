from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLE = (
        (USER, 'User role'),
        (MODERATOR, 'Moderator role'),
        (ADMIN, 'Administrator role'),
    )

    role = models.CharField(
        'Пользовательская роль',
        max_length=2,
        choices=USER_ROLE,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
