from django import forms
from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"Запрещенное слово в названии: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f"Запрещенное слово в описании: {word}")
        return description
