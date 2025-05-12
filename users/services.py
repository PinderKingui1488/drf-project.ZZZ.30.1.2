import stripe
from config.settings import API_KEY
from rest_framework.exceptions import ValidationError

stripe.api_key = API_KEY


def create_stripe_product(payment):
    try:
        return stripe.Product.create(
            name=f"{payment.course if payment.course else payment.lesson}",
            description=f"Payment for {payment.course if payment.course else payment.lesson}"
        )
    except stripe.error.StripeError as e:
        raise ValidationError(f"Error creating Stripe product: {str(e)}")


def create_price(amount, product):
    try:
        return stripe.Price.create(
            currency="rub",
            unit_amount=amount * 100,
            product=product.get("id"),
            metadata={
                "product_type": "course" if product.get("name").startswith("Course") else "lesson"
            }
        )
    except stripe.error.StripeError as e:
        raise ValidationError(f"Error creating Stripe price: {str(e)}")


def create_stripe_session(price):
    try:
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/payment/success/",
            cancel_url="http://127.0.0.1:8000/payment/cancel/",
            line_items=[{"price": price.get("id"), "quantity": 1}],
            mode="payment",
            payment_method_types=['card'],
            metadata={
                "price_id": price.get("id")
            }
        )
        return session.get("id"), session.get("url")
    except stripe.error.StripeError as e:
        raise ValidationError(f"Error creating Stripe session: {str(e)}")