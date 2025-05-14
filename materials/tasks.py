from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_course_update_email(course_id, emails):
    from materials.models import Course  # импорт внутри задачи, чтобы избежать циклических импортов
    course = Course.objects.get(pk=course_id)
    subject = f"Обновление материалов курса: {course.name}"
    message = f"В курсе '{course.name}' появились новые материалы!"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False,
    )
