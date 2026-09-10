from django import forms
from catalog.models import Product, ProductPrice, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'brand', 'product_type', 'stock', 'is_active', 'base_image']


class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = ['price', 'discount_percent']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='نام')
    email = forms.EmailField(label='ایمیل')
    subject = forms.CharField(max_length=200, label='موضوع')
    message = forms.CharField(widget=forms.Textarea, label='پیام')

