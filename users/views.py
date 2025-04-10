from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializer import PaymentsSerializers, UserSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['paid_course', 'separately_paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()