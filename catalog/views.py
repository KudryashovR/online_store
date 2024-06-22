from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from catalog.models import Product, Contact, Category


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


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'preview', 'category', 'price')
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('id')

        return context
