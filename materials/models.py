from django.db import models
from django.utils import timezone


class Course(models.Model):
    objects = None
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Хозяин",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def str(self):
        return self.name


class Lesson(models.Model):
    objects = None
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
    )
    description = models.TextField(
        verbose_name="Внешка",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="lessons",
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Хозяин",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
        permissions = []

    def str(self):
        return self.name



class Subscription(models.Model):
    objects = None
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def str(self):
        return f'subscription {self.pk}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'