from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse




# News
class News(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_date = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return self.name
    

# Blog Category Model
class BlogCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_date = models.DateTimeField(default=now, blank=True, null=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


# Blog Model
class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    description = RichTextField()  # CKEditor RichTextField
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_date = models.DateTimeField(default=now, blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title


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

    def get_absolute_url(self):
        return reverse('service_details', args=[self.slug])


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
    

class PricingSection(models.Model):
    title = models.CharField(
        max_length=255,
        default="Flexible Pricing Plans",
        help_text="Main title for the pricing section"
    )
    description = models.TextField(
        blank=True,
        default="Choose from our tailored plans designed to meet your business needs.",
        help_text="Short description under the title"
    )

    def __str__(self):
        return self.title


class PricingPlan(models.Model):
    section = models.ForeignKey(
        PricingSection,
        on_delete=models.CASCADE,
        related_name="plans"
    )
    title = models.CharField(
        max_length=100,
        help_text="Plan name (e.g., Starter, Standard, Pro)"
    )
    description = models.TextField(
        blank=True,
        help_text="Short tagline for the plan"
    )

    def __str__(self):
        return self.title


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name="features"
    )
    text = models.CharField(
        max_length=255,
        help_text="Feature description (Admin can add any number of features)"
    )

    def __str__(self):
        return f"{self.plan.title} - {self.text}"




# Cost Calculator 
class CostCalculatorEnquiry(models.Model):
    business_activity = models.CharField(max_length=255)
    jurisdiction = models.CharField(max_length=100)
    sponsorship = models.CharField(max_length=10, blank=True, null=True)
    owners = models.CharField(max_length=50)
    visas = models.CharField(max_length=10)
    office_required = models.CharField(max_length=10)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.business_activity}"

#Cotnact
class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class ServiceEnquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_name}"



# Team
class Team(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name
    
# client Logo
class ClientLogo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='client_logos/')

    def __str__(self):
        return self.name