from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



# materials/models.py
from django.db import models
from users.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons') # Ссылка на курс

    def __str__(self):
        return self.title

class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('materials.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments') # Добавим связь с курсом, за который платили
    lesson = models.ForeignKey('materials.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments') # Добавим связь с уроком, за который платили

    def __str__(self):
        return f"Payment from {self.user.email} for {self.amount}"