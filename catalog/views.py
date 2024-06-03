from django.shortcuts import render

import datetime

from catalog.models import Product


def home(request):
    latest_products = Product.objects.order_by('-id')[:5]

    for product in latest_products:
        print(
            f'Product ID: {product.id}, Name: {product.name}, Description: {product.description}, '
            f'Price: {product.price}'
        )

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

    return render(request, 'catalog/contacts.html')
