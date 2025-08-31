from django import forms

from .models import Menu, Category, Service, ContactModel, NearByPlace, ClientReview, ServiceProcessStep, ServiceFAQ
from ckeditor.widgets import CKEditorWidget  



# Contact us
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'

# NearByPlaceForm
class NearByPlaceForm(forms.ModelForm):
    class Meta:
        model = NearByPlace
        fields = '__all__'

# Clien Review
class ClientReviewForm(forms.ModelForm):
    class Meta:
        model = ClientReview
        fields = '__all__'


from django.utils.text import slugify
from .models import Menu, Category, Service

# Menu Form
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'slug', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Menu Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order'}),
        }


# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['menu', 'name', 'slug', 'order']
        widgets = {
            'menu': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order'}),
        }

# Service Form
class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())  # Use CKEditor widget

    class Meta:
        model = Service
        fields = ['category', 'name', 'slug', 'description', 'image', 'order']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order'}),
        }

# Service Process Step Form
class ServiceProcessStepForm(forms.ModelForm):
    class Meta:
        model = ServiceProcessStep
        fields = ['step_number', 'title', 'description']
        widgets = {
            'step_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Step Number'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Step Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Step Description'}),
        }

# Service FAQ Form
class ServiceFAQForm(forms.ModelForm):
    class Meta:
        model = ServiceFAQ
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FAQ Question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'FAQ Answer'}),
        }