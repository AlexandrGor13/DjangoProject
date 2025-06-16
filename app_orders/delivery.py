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
    address_line1 = request.POST.get('address_line1')
    address_line2 = request.POST.get('address_line2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    country = request.POST.get('country')
    address = DeliveryAddress(
        user=current_user,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        state=state,
        zip_code=zip_code,
        country=country,
        default=True
    )
    address.save()
    return address
