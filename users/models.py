from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Введите почту",
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватарка",
        help_text="Вставьте аватарку",
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город проживания",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email