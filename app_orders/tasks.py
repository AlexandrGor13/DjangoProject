from celery import shared_task
from django_celery_beat.models import PeriodicTask
from yookassa import Payment

from .models import Payment as PaymentModel
from .order import update_quantity_after_order


@shared_task(name="repeat_payment_make")
def repeat_order_make(payment_id, transaction_id):
    """Проверка статуса платежа"""
    payment = Payment.find_one(payment_id=transaction_id)
    if payment.status == "succeeded":
        payment_m = PaymentModel.objects.get(id=payment_id)
        payment_m.status = "paid"
        payment_m.save()
        update_quantity_after_order
        task = PeriodicTask.objects.get(
            name="Repeat order {}".format(payment_m.order.id)
        )
        task.delete()
