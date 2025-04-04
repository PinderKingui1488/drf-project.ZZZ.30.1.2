from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Введите название курса"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание курса"
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Вставьте изображение курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание урока"
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение урока",
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="В каком курсе урок?"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
        permissions = []

    def __str__(self):
        return self.name