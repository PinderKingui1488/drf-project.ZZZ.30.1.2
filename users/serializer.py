from materials.validators import YoutubeURLValidator
from materials.models import Course, Lesson, Subscription
from rest_framework import serializers
from django.db.models import Count


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True) # Для создания урока
    video_link = serializers.URLField(validators=[YoutubeURLValidator()]) # Валидация URL

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True) # Подсчет уроков через annotate
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_queryset(self):
        return Course.objects.annotate(lesson_count=Count('lessons')) # annotate для подсчета

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()


class SubscriptionSerializer(serializers.ModelSerializer): # Переименовано
    class Meta:
        model = Subscription
        fields = "__all__"


