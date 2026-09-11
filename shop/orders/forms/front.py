from django import forms


class FakePaymentForm(forms.Form):
    card_number = forms.CharField(
        label="شماره کارت", max_length=19,
        widget=forms.TextInput(attrs={"placeholder": "6219-8619-9999-4445", "inputmode": "numeric"}),
    )
    card_holder = forms.CharField(label="نام صاحب کارت", max_length=120)
    cvv2 = forms.CharField(
        label="CVV2", max_length=4,
        widget=forms.TextInput(attrs={"placeholder": "123", "inputmode": "numeric"}),
    )
    expire_month = forms.CharField(label="ماه انقضا", max_length=2, widget=forms.TextInput(attrs={"placeholder": "09"}))
    expire_year = forms.CharField(label="سال انقضا", max_length=2, widget=forms.TextInput(attrs={"placeholder": "05"}))
    otp = forms.CharField(
        label="رمز پویا", max_length=8,
        widget=forms.TextInput(attrs={"placeholder": "------", "inputmode": "numeric"}),
    )

    def clean_card_number(self):
        number = self.cleaned_data["card_number"].replace("-", "").replace(" ", "")
        if not number.isdigit() or len(number) < 12:
            raise forms.ValidationError("شماره کارت معتبر نیست")
        return number
