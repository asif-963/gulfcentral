from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone


# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Contact"
    

# Near By Places
class NearByPlace(models.Model):
    name = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Place_images/',blank=True, null=True)
    created_date = models.DateTimeField(default=now,blank=True, null=True)

    def __str__(self):
        return self.name


# Client Reviews
class ClientReview(models.Model):
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_image = models.ImageField(upload_to='client_images/', null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.client_name} - {self.designation}"


# Servieces
class Menu(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Category(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('menu', 'slug')

    def __str__(self):
        return f"{self.menu.name} → {self.name}"


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='services/images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('category', 'slug')

    def __str__(self):
        return f"{self.category.menu.name} → {self.category.name} → {self.name}"


class ServiceProcessStep(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="process_steps")
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.service.name} - Step {self.step_number}: {self.title}"


class ServiceFAQ(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="faqs")
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for {self.service.name}: {self.question[:50]}..."

        





