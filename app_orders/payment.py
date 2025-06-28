import json

from django.conf import settings
from django.utils.timezone import now
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from yookassa import Configuration, Payment

from app_orders.models import Payment as PaymentModel
from app_orders.order import get_last_order

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_order_payment(request):
    order = get_last_order(request)
    transaction_id = None
    payment_url = "/"
    payment = PaymentModel.objects.filter(order=order).first()
    if not payment:
        payment = PaymentModel.objects.create(
            order=order,
            amount=order.total_amount,
            transaction_id=transaction_id,
        )
        payment_data = create_payment(request, payment)

        if payment_data:
            payment_id = payment_data.get("id")
            payment_url = (payment_data.get("confirmation")).get("confirmation_url")
            payment.transaction_id = payment_id
            payment.save()
    return payment_url


def create_payment(request, payment):
    try:
        if payment.status != "pending":
            return None
        payment_data = {
            "amount": {"value": str(payment.amount), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": f"http://{request.get_host()}/order/payment/status/?id={payment.id}",
            },
            "capture": True,
            "description": f"Оплата заказа № {payment.order.id}",
            "metadata": {
                "order_id": payment.order.id,
            },
        }
        payment = Payment.create(payment_data)
        payment_data = json.loads(payment.json())
        return payment_data
    except Exception as e:
        return None


def get_status_payment(payment_m: PaymentModel):
    status = None
    try:
        payment_id = payment_m.transaction_id
        payment = Payment.find_one(payment_id=payment_id)
        if payment.status == "succeeded":
            status = "paid"
        elif payment.status == "canceled":
            status = "canceled"
        else:
            status = "pending"
            try:
                PeriodicTask.objects.create(
                    name="Repeat order {}".format(payment_m.order.id),
                    task="repeat_payment_make",
                    interval=IntervalSchedule.objects.get(every=10, period="seconds"),
                    args=json.dumps([payment_m.id, payment_id]),
                    start_time=now(),
                )
            except Exception as e:
                print(e)
        payment_m.status = status
        payment_m.save()
        return status
    except Exception as e:
        return status
