from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from addresses.models import Address


@user_passes_test(lambda u: u.is_staff)
def address_list(request):
    addresses = Address.objects.select_related("user").order_by("-updated_time")
    return render(request, "addresses/panel/address_list.html", {"addresses": addresses})
