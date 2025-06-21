from django.template.defaultfilters import default

from app_users.user import get_current_user
from app_orders.models import Order, DeliveryAddress


def get_address(request):
    current_user = get_current_user(request)
    address = DeliveryAddress.objects.filter(user=current_user, default=True).first()
    # if not address:
    #     return create_address(request)
    return address


def create_address(request):
    current_user = get_current_user(request)
    address_line = request.POST.get('address_line')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    country = request.POST.get('country')
    address = DeliveryAddress(
        user=current_user,
        address_line=address_line,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        default=True
    )
    address.save()
    return address
