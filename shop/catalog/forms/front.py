from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="نام و نام خانوادگی", max_length=120)
    email = forms.EmailField(label="ایمیل")
    subject = forms.CharField(label="موضوع", max_length=150)
    message = forms.CharField(label="متن پیام", widget=forms.Textarea(attrs={"rows": 5}))
