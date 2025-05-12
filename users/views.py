from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone
from users.models import Payments, User
from users.serializer import PaymentsSerializers, UserSerializer
from users.services import create_price, create_stripe_product, create_stripe_session
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
from config.settings import API_KEY

stripe.api_key = API_KEY


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['paid_course', 'separately_paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user, date=timezone.now().date())
        product = create_stripe_product(payment)
        price = create_price(payment.payment_summ, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, API_KEY
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment = Payments.objects.get(session_id=session['id'])
        payment.payment_status = 'completed'
        payment.save()

    return HttpResponse(status=200)


class PaymentSuccessView(APIView):
    def get(self, request):
        return Response({"message": "Payment successful!"})


class PaymentCancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment cancelled"})