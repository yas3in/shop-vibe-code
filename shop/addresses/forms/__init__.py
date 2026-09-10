from django import forms
from addresses.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['receipt_name', 'phone_number', 'city', 'postal_code', 'full_address', 'address_detail', 'is_default']

