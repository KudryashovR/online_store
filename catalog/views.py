from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Category, Blog, ProductVersion


class ProductListView(ListView):
    model = Product
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_versions = []

        for product in Product.objects.all():
            current_version = product.versions.filter(is_current=True).first()
            products_with_versions.append((product, current_version))
        context['products_with_versions'] = products_with_versions

        return context


class ContactView(TemplateView):
    model = Contact
    template_name = 'catalog/contact_list.html'

    def post(self, request):
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
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_version = self.object.versions.filter(is_current=True).first()
        context['product_version'] = current_version

        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, ProductVersion, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = SubjectFormset(self.request.POST)
        else:
            context['formset'] = SubjectFormset()

        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, ProductVersion, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = SubjectFormset(instance=self.object)

        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        active_versions_count = ProductVersion.objects.filter(product=self.object, is_current=True).count()

        if active_versions_count > 1:
            form.add_error(None, 'Допустима только одна активная версия для каждого продукта.')

            return self.form_invalid(form)

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class BlogListView(ListView):
    model = Blog
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('catalog:blog')


class BlogDetailView(DetailView):
    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, *args, **kwargs):
        article = super().get_object(*args, **kwargs)
        article.views_count += 1
        article.save()

        return article


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('catalog:blog_detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
