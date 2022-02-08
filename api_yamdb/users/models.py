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
        max_length=15,
        choices=USER_ROLE,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.email
