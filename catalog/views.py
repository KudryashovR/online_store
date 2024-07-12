from datetime import datetime

from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.mixins import CustomLoginRequiredMixin
from catalog.models import Product, Contact, Blog, ProductVersion


class ProductListView(CustomLoginRequiredMixin, ListView):
    """
    Класс-представление для отображения списка продуктов.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    ListView (ListView): Базовое представление для отображения списка объектов.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление списка (Product).
    paginate_by (int): Количество объектов на одной странице (по умолчанию 10).

    Методы:
    get_context_data(**kwargs) (dict): Переопределенный метод для добавления дополнительного контекста (список продуктов
                                       с их текущими версиями).
    """

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


class ContactView(CustomLoginRequiredMixin, TemplateView):
    """
    Класс-представление для отображения и обработки формы контактов.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    TemplateView (TemplateView): Базовое представление для отображения HTML-шаблона.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Contact).
    template_name (str): Имя HTML-шаблона для отображения контактов.

    Методы:
    post(request) (HttpResponse): Метод для обработки POST-запросов, сохраняет отправленные данные в файл и возвращает
                                  ответ.
    get_context_data(**kwargs) (dict): Переопределенный метод для добавления дополнительного контекста (список
                                       контактов).
    """

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


class ProductDetailView(CustomLoginRequiredMixin, DetailView):
    """
    Класс-представление для отображения деталей продукта.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    DetailView (DetailView): Базовое представление для отображения деталей объекта.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Product).
    form_class (ModelForm): Форма, используемая для взаимодействия с моделью продукта.

    Методы:
    get_context_data(**kwargs) (dict): Переопределенный метод для добавления дополнительного контекста (текущая версия
                                       продукта).
    """

    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_version = self.object.versions.filter(is_current=True).first()
        context['product_version'] = current_version

        return context


class ProductCreateView(CustomLoginRequiredMixin, CreateView):
    """
    Класс-представление для создания нового продукта.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    CreateView (CreateView): Базовое представление для создания нового объекта.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Product).
    form_class (ModelForm): Форма, используемая для создания объекта продукта.
    success_url (str): URL перенаправления после успешного создания объекта.

    Методы:
    get_context_data(**kwargs) (dict): Переопределенный метод для добавления дополнительного контекста (набор форм
                                       версий продукта).
    form_valid(form) (HttpResponse): Переопределенный метод для обработки валидной формы и сохранения объекта
                                     и его версий.
    """

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


class ProductUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    Класс-представление для обновления существующего продукта.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    UpdateView (UpdateView): Базовое представление для обновления существующего объекта.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Product).
    form_class (ModelForm): Форма, используемая для обновления объекта продукта.
    success_url (str): URL перенаправления после успешного обновления объекта.

    Методы:
    get_context_data(**kwargs) (dict): Переопределенный метод для добавления дополнительного контекста (набор форм
                                       версий продукта).
    form_valid(form) (HttpResponse): Переопределенный метод для обработки валидной формы и сохранения объекта
                                     и его версий. Проверяет, чтобы была только одна активная версия продукта.
    """

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


class ProductDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления существующего продукта.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    DeleteView (DeleteView): Базовое представление для удаления существующего объекта.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Product).
    success_url (str): URL перенаправления после успешного удаления объекта.
    """

    model = Product
    success_url = reverse_lazy('catalog:home')


class BlogListView(CustomLoginRequiredMixin, ListView):
    """
    Класс-представление для отображения списка опубликованных блогов.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    ListView (ListView): Базовое представление для отображения списка объектов.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Blog).
    paginate_by (int): Количество объектов на одной странице (по умолчанию 10).

    Методы:
    get_queryset(): Возвращает QuerySet из опубликованных блогов.
    """

    model = Blog
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CustomLoginRequiredMixin, CreateView):
    """
    Класс-представление для создания нового блога.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    CreateView (CreateView): Базовое представление для создания модели.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Blog).
    fields (tuple): Поля модели, которые будут использоваться в форме создания блога (title, content, preview,
                    is_published).
    success_url (str): URL, на который будет перенаправлен пользователь после успешного создания блога.
    """

    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('catalog:blog')


class BlogDetailView(CustomLoginRequiredMixin, DetailView):
    """
    Класс-представление для отображения деталей отдельного блога.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    DetailView (DetailView): Базовое представление для отображения деталей объекта модели.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Blog).
    slug_field (str): Поле модели, которое будет использоваться для поиска объекта (slug).
    slug_url_kwarg (str): Параметр URL, который будет использоваться для поиска объекта по полю slug.

    Методы:
    get_object(*args, **kwargs): Переопределяет метод получения объекта для увеличения счетчика просмотров статьи.
    """

    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, *args, **kwargs):
        article = super().get_object(*args, **kwargs)

        article.views_count += 1
        article.save()

        return article


class BlogUpdateView(CustomLoginRequiredMixin, UpdateView):
    """
    Класс-представление для обновления существующей записи блога.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    UpdateView (UpdateView): Базовое представление для обновления объекта модели.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Blog).
    fields (tuple): Поля модели, которые будут отображаться в форме для обновления записи.
    slug_field (str): Поле модели, которое будет использоваться для поиска объекта (slug).
    slug_url_kwarg (str): Параметр URL, который будет использоваться для поиска объекта по полю slug.

    Методы:
    get_success_url(): Возвращает URL для перенаправления после успешного обновления записи блога.
    """

    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('catalog:blog_detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления записи блога.

    Наследует:
    CustomLoginRequiredMixin (миксин): Обеспечивает доступ к представлению только для авторизованных пользователей.
    DeleteView (DeleteView): Базовое представление для удаления объекта модели.

    Атрибуты класса:
    model (Model): Модель, для которой создается представление (Blog).
    success_url (str): URL, на который будет перенаправлен пользователь после успешного удаления записи.
    slug_field (str): Поле модели, которое используется для поиска объекта (slug).
    slug_url_kwarg (str): Параметр URL, который используется для поиска объекта по полю slug.
    """

    model = Blog
    success_url = reverse_lazy('catalog:blog')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
