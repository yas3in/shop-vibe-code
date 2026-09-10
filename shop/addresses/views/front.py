from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from addresses.models import Address
from addresses.forms import AddressForm


@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'addresses/address_list.html', {'addresses': addresses})


@login_required
def address_create(request):
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            if next_url:
                return redirect(next_url)
            return redirect('addresses:address_list')
    else:
        form = AddressForm()
    return render(request, 'addresses/address_form.html', {'form': form, 'next_url': next_url})


@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).exclude(pk=pk).update(is_default=False)
            address.save()
            return redirect('addresses:address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'addresses/address_form.html', {'form': form})


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
    return redirect('addresses:address_list')
