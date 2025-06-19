from django import forms
from .models import Space
from django.core.exceptions import ValidationError

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        price_hour = cleaned_data.get('price_per_hour')
        price_day = cleaned_data.get('price_per_day')
        price_month = cleaned_data.get('price_per_month')

        if price_hour is not None and price_hour < 0:
            self.add_error('price_per_hour', 'El precio por hora debe ser positivo')

        if price_day is not None and price_day < 0:
            self.add_error('price_per_day', 'El precio por día debe ser positivo')

        if price_month is not None and price_month < 0:
            self.add_error('price_per_month', 'El precio por mes debe ser positivo')

        capacity = cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            self.add_error('capacity', 'La capacidad debe ser mayor a 0')

        # Aquí podrías agregar más validaciones si quieres

        return cleaned_data
