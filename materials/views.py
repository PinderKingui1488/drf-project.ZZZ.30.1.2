from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from materials.paginators import CustomPaginator
from materials.models import Lesson, Course, Subscription
from materials.serializer import LessonSerializer, LessonDetailSerializer, CourseSerializer
from users.permissions import IsModer, IsOwner
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


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