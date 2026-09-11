from django.contrib import messages
from django.shortcuts import redirect, render

from catalog.forms import ContactForm
from catalog.models import Brand, Product
from core.models import ContactMessage


def home(request):
    top_selling = Product.objects.filter(is_active=True).select_related(
        "price", "brand", "category"
    ).order_by("-sold_count")[:8]
    most_discounted = Product.objects.filter(
        is_active=True, price__discount_percent__gt=0
    ).select_related("price", "brand", "category").order_by("-price__discount_percent")[:8]
    brands = Brand.objects.filter(is_active=True)
    return render(request, "core/home.html", {
        "top_selling": top_selling,
        "most_discounted": most_discounted,
        "brands": brands,
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
            )
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
