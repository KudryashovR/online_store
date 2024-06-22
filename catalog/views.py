from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import ListView, TemplateView, DetailView

from catalog.models import Product, Category, ProductForm, Contact


class ProductListView(ListView):
    model = Product
    paginate_by = 10


class ContactView(TemplateView):
    model = Contact
    template_name = 'catalog/contact_list.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            with open('messages.txt', 'a+', encoding='utf-8') as file:
                file.write(f"{datetime.now()} - {name} ({phone}): {message}\n")

        contact_details = Contact.objects.all()
        context = {
            'object_list': contact_details,
        }

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Contact.objects.all()

        return context


class ProductDetailView(DetailView):
    model = Product


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
