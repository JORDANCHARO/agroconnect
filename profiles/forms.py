from django import forms
from .models import ProducerProfile, ProcessorProfile, Product, ProductionEvent

class ProducerProfileForm(forms.ModelForm):
    class Meta:
        model = ProducerProfile
        fields = ['farm_name', 'farm_description', 'location', 'latitude', 'longitude', 'certification_documents']
        widgets = {
            'farm_description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }

class ProcessorProfileForm(forms.ModelForm):
    class Meta:
        model = ProcessorProfile
        fields = ['company_name', 'company_description', 'location', 'certification_documents', 
                 'transformation_capacity', 'transformed_products']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'transformation_capacity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1000 tonnes/an'
            }),
            'transformed_products': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Listez vos produits transformés (un par ligne)'
            }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'unit', 'price_per_unit', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductionEventForm(forms.ModelForm):
    class Meta:
        model = ProductionEvent
        fields = ['title', 'description', 'event_type', 'start_date', 'end_date', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        } 