from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import datetime

from catalog.models import Product, Contact, Category, ProductForm


def home(request):
    products_list = Product.objects.all().order_by('id')
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
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


def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')
    else:
        categories = Category.objects.all().order_by('id')
        context = {
            'categories': categories
        }

        return render(request, 'catalog/new_product.html', context)
