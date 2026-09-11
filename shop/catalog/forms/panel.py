from django import forms

from catalog.models import Product, ProductImage, ProductPrice


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(item, initial) for item in data]
        return super().clean(data, initial)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "category", "brand", "product_type", "stock", "is_active", "base_image"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = ["price", "discount_percent"]


class ProductImageForm(forms.ModelForm):
    gallery = MultipleFileField(label="تصاویر گالری", required=False, widget=MultipleFileInput)

    class Meta:
        model = ProductImage
        fields = []
