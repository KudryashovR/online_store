from django.shortcuts import render

import datetime


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        with open('messages.txt', 'a+', encoding='utf-8') as file:
            file.write(f"{datetime.datetime.now()} - {name} ({phone}): {message}\n")

    return render(request, 'catalog/contacts.html')
