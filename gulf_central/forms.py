from django import forms

from .models import Menu, Category, Service, ContactModel, News, ClientReview, ServiceProcessStep, ServiceFAQ, BlogCategory, Blog
from ckeditor.widgets import CKEditorWidget  



# Contact us
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'

# NewsForm
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
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
    description = forms.CharField(widget=CKEditorWidget(), required=False)

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


# Blog Category Form
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Category Name', 'required': True}),
        }


# Blog Form
class BlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ['category', 'title', 'description', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }