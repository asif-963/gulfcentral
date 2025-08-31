from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import random

from .models import Menu, Category, Service, ContactModel, NearByPlace, ClientReview, ServiceProcessStep, ServiceFAQ
from .forms import ContactModelForm, NearByPlaceForm, MenuForm, CategoryForm, ServiceForm, ClientReviewForm, ServiceProcessStepForm, ServiceFAQForm







def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def service_details(request):
    return render(request, 'service-details.html')

def contact(request):
    return render(request, 'contact.html')



# Admin Side
@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:   
            messages.error(request, "There was an error logging in, try again.")
            return redirect('login')
    return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('index')


#  dashboard
@login_required(login_url='user_login')
def dashboard(request):
    return render(request,'admin_pages/dashboard.html')


# Contact 
@login_required(login_url='user_login')
def contact_view(request):
    contacts = ContactModel.objects.all().order_by('-id')
    return render(request,'admin_pages/contact_view.html',{'contacts':contacts})


@login_required(login_url='user_login')
def delete_contact(request,id):
    contact = ContactModel.objects.get(id=id)
    contact.delete()
    return redirect('contact_view')



# Client Reviews
@login_required(login_url='user_login')
def add_client_review(request):
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews') 
    else:
        form = ClientReviewForm()

    return render(request, 'admin_pages/add_client_review.html', {'form': form})


@login_required(login_url='user_login')
def view_client_reviews(request):
    client_reviews = ClientReview.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_client_reviews.html', {'client_reviews': client_reviews})


@login_required(login_url='user_login')
def update_client_review(request, id):
    client_reviews = get_object_or_404(ClientReview, id=id)
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES, instance=client_reviews)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews')
    else:
        form = ClientReviewForm(instance=client_reviews)
    return render(request, 'admin_pages/update_client_review.html', {'form': form, 'client_reviews': client_reviews})

    

@login_required(login_url='user_login')
def delete_client_review(request,id):
    client_reviews = ClientReview.objects.get(id=id)
    client_reviews.delete()
    return redirect('view_client_reviews')



# Near by place
@login_required(login_url='user_login')
def add_near_by_place(request):
    if request.method == 'POST':
        form = NearByPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_near_by_place') 
    else:
        form = NearByPlaceForm()

    return render(request, 'admin_pages/add_near_by_place.html', {'form': form})


@login_required(login_url='user_login')
def view_near_by_place(request):
    places = NearByPlace.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_near_by_place.html', {'places': places})


@login_required(login_url='user_login')
def update_near_by_place(request, id):
    place = get_object_or_404(NearByPlace, id=id)
    if request.method == 'POST':
        form = NearByPlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('view_near_by_place')
    else:
        form = NearByPlaceForm(instance=place)
    return render(request, 'admin_pages/update_near_by_place.html', {'form': form, 'place': place})

@login_required(login_url='user_login')
def delete_near_by_place(request,id):
    places = NearByPlace.objects.get(id=id)
    places.delete()
    return redirect('view_near_by_place')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})



# ----------------------------
# MENUS
# ----------------------------
def view_menus(request):
    menus = Menu.objects.all()
    return render(request, "admin_pages/view_menus.html", {"menus": menus})

def add_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_menus')
    else:
        form = MenuForm()
    return render(request, "admin_pages/add_menus.html", {"form": form})

def update_menu(request, pk):
    menu = get_object_or_404(Menu, id=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('view_menus')
    else:
        form = MenuForm(instance=menu)
    # Pass the menu object to template so values show
    return render(request, "admin_pages/update_menu.html", {"menu": menu, "form": form})


def delete_menu(request, pk):
    menu = get_object_or_404(Menu, id=pk)
    menu.delete()
    return redirect('view_menus')


# ----------------------------
# Category
# ----------------------------

# Add Category
def add_category(request):
    menus = Menu.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = CategoryForm()
    return render(request, "admin_pages/add_category.html", {"form": form, "menus": menus})

# View Categories
def view_categories(request):
    categories = Category.objects.all().order_by('order')
    return render(request, "admin_pages/view_categories.html", {"categories": categories})

# Update Category
def update_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    menus = Menu.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, "admin_pages/update_category.html", {"category": category, "menus": menus, "form": form})

# Delete Category
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect('view_categories')


# View all services
def view_services(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'admin_pages/view_services.html', {'services': services})

# Add service
def add_service(request):
    categories = Category.objects.all().order_by('menu', 'order')
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()

            # Save new process steps
            for key in request.POST:
                if key.startswith('new_step_title_'):
                    step_num = key.split('_')[-1]
                    title = request.POST.get(f'new_step_title_{step_num}')
                    description = request.POST.get(f'new_step_description_{step_num}')
                    if title and description:
                        ServiceProcessStep.objects.create(service=service, step_number=int(step_num), title=title, description=description)

            # Save new FAQs
            for key in request.POST:
                if key.startswith('new_faq_question_'):
                    faq_num = key.split('_')[-1]
                    question = request.POST.get(f'new_faq_question_{faq_num}')
                    answer = request.POST.get(f'new_faq_answer_{faq_num}')
                    if question and answer:
                        ServiceFAQ.objects.create(service=service, question=question, answer=answer)

            return redirect('view_services')
    else:
        form = ServiceForm()
    return render(request, 'admin_pages/add_service.html', {'form': form, 'categories': categories})

# Update service
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    categories = Category.objects.all().order_by('menu', 'order')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save()

            # Update existing process steps
            for step in service.process_steps.all():
                title = request.POST.get(f'step_title_{step.id}')
                description = request.POST.get(f'step_description_{step.id}')
                if title and description:
                    step.title = title
                    step.description = description
                    step.save()

            # Add new process steps
            existing_step_count = service.process_steps.count()
            step_count = existing_step_count
            for key in request.POST:
                if key.startswith('new_step_title_'):
                    step_count += 1
                    title = request.POST.get(f'new_step_title_{step_count}')
                    description = request.POST.get(f'new_step_description_{step_count}')
                    if title and description:
                        ServiceProcessStep.objects.create(service=service, step_number=step_count, title=title, description=description)

            # Update existing FAQs
            for faq in service.faqs.all():
                question = request.POST.get(f'faq_question_{faq.id}')
                answer = request.POST.get(f'faq_answer_{faq.id}')
                if question and answer:
                    faq.question = question
                    faq.answer = answer
                    faq.save()

            # Add new FAQs
            existing_faq_count = service.faqs.count()
            faq_count = existing_faq_count
            for key in request.POST:
                if key.startswith('new_faq_question_'):
                    faq_count += 1
                    question = request.POST.get(f'new_faq_question_{faq_count}')
                    answer = request.POST.get(f'new_faq_answer_{faq_count}')
                    if question and answer:
                        ServiceFAQ.objects.create(service=service, question=question, answer=answer)

            return redirect('view_services')

    else:
        form = ServiceForm(instance=service)

    return render(request, 'admin_pages/update_services.html', {'form': form, 'service': service, 'categories': categories})

# Delete service
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('view_services')