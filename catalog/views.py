from django.shortcuts import render, get_object_or_404

import datetime

from catalog.models import Product, Contact


def home(request):
    latest_products = Product.objects.order_by('-id')[:100]
    context = {
        'products': latest_products,
    }

    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        with open('messages.txt', 'a+', encoding='utf-8') as file:
            file.write(f"{datetime.datetime.now()} - {name} ({phone}): {message}\n")

    contact_details = Contact.objects.all()
    context = {
        'contact_details': contact_details,
    }

    return render(request, 'catalog/contacts.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }

    return render(request, 'catalog/product_detail.html', context)
