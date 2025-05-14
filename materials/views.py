from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from materials.paginators import CustomPaginator
from materials.models import Lesson, Course, Subscription
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from materials.serializer import LessonSerializer, LessonDetailSerializer, CourseSerializer
from users.permissions import IsModer, IsOwner
from django.utils import timezone
from datetime import timedelta
from materials.tasks import send_course_update_email

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPaginator
    serializer_class = CourseSerializer

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        now = timezone.now()
        # Проверка: прошло ли больше 4 часов с последнего обновления
        if instance.updated_at is None or (now - instance.updated_at) > timedelta(hours=4):
            # Получаем email всех подписчиков
            emails = list(
                Subscription.objects.filter(course=instance, user__email__isnull=False)
                .values_list('user__email', flat=True)
            )
            if emails:
                send_course_update_email.delay(instance.pk, emails)
        return super().update(request, *args, **kwargs)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer, IsAuthenticated)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsOwner, IsAuthenticated)


class SubView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course, pk=self.request.data.get('course_id'))

        subs_item = Subscription.objects.filter(user=user, course=course).first()

        if subs_item:
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        return Response({"message": message})


class HomeView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            "message": "Welcome to DRF Project API",
            "endpoints": {
                "courses": "/courses/",
                "lessons": "/lessons/",
                "users": "/users/",
                "swagger": "/swagger/",
                "redoc": "/redoc/"
            }
        })