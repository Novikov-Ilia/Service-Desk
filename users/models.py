from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        SUPPORT = 'support', 'Поддержка'
        MANAGER = 'manager', 'Менеджер'
        ADMIN = 'admin', 'Администратор'
        
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT, 
    )