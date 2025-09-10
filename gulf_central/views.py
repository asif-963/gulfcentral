from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import random

from .models import Menu, Category, Service, ContactModel, News, ClientReview, ServiceProcessStep, ServiceFAQ, BlogCategory, Blog
from .forms import ContactModelForm, NewsForm, MenuForm, CategoryForm, ServiceForm, ClientReviewForm, BlogCategoryForm, BlogForm







def index(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    client_reviews = ClientReview.objects.all()
    latest_news = News.objects.order_by('-created_date')[:3]
    services = Service.objects.values_list('name', flat=True)  
    categories = list(Category.objects.prefetch_related('services').all())
    random.shuffle(categories)       # Shuffle all categories
    categories = categories[:6]   
    return render(request, 'index.html', {'menus': menus, 'client_reviews':client_reviews, 'latest_news':latest_news, 'categories': categories,'services':list(services)})


def about(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    client_reviews = ClientReview.objects.all()
    return render(request, 'about.html',{'menus': menus, 'client_reviews':client_reviews})


# News listing page
def news(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    news_items = News.objects.order_by('-created_date')  # Latest news first
    context = {'menus': menus, 'news_items': news_items}
    return render(request, 'news.html', context)

# News details page
def news_detail(request, pk):
    menus = Menu.objects.prefetch_related('categories__services').all()
    news_item = get_object_or_404(News, pk=pk)
    latest_news = News.objects.exclude(pk=pk).order_by('-created_date')[:5]
    context = {'news': news_item, 'menus': menus, 'latest_news':latest_news}
    return render(request, 'news-details.html', context)


def blogs(request):
    menus = Menu.objects.prefetch_related('categories__services').all()

    query = request.GET.get("q")
    category_id = request.GET.get("category")

    blogs = Blog.objects.all().order_by("-created_date")

    # Search filter
    if query:
        blogs = blogs.filter(title__icontains=query)

    # Category filter
    if category_id:
        blogs = blogs.filter(category_id=category_id)

    categories = BlogCategory.objects.all()

    return render(request, "blogs.html", {
        "menus": menus,
        "blogs": blogs,
        "categories": categories,
        "query": query,
    })
def blog_detail(request, pk):
    menus = Menu.objects.prefetch_related('categories__services').all()
    blog = get_object_or_404(Blog, pk=pk)
    latest_blogs = Blog.objects.exclude(pk=pk)[:3]  # 3 latest posts excluding current
    categories = BlogCategory.objects.all()
    
    return render(request, "blog-details.html", {
        "menus": menus,
        "blog": blog,
        "latest_blogs": latest_blogs,
        "categories": categories,
    })



def cost_calculator(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'cost-calculator.html',{'menus': menus})

def mainland(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'mainland-details.html',{'menus': menus})

def freezone(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'freezone-details.html',{'menus': menus})

def offshore(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'offshore-details.html',{'menus': menus})

def service_details(request, slug):
    menus = Menu.objects.prefetch_related('categories__services').all()
    # Get the service object
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.filter(category=service.category).exclude(id=service.id)
    process_steps = ServiceProcessStep.objects.filter(service=service).order_by('step_number')
    faqs = ServiceFAQ.objects.filter(service=service)

    context = {
        'service': service,
        'process_steps': process_steps,
        'faqs': faqs,
        'related_services': related_services,
        'menus': menus,
    }
    return render(request, 'service-details.html', context)

def terms_and_conditions(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'terms_and_conditions.html',{'menus': menus})

def privacy_and_policy(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'privacy_and_policy.html',{'menus': menus})


def contact(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    return render(request, 'contact.html',{'menus': menus})




from django.http import JsonResponse
from .models import Service

def ajax_search_services(request):
    query = request.GET.get('q', '').strip()
    if query:
        services = Service.objects.filter(name__icontains=query)[:10]
        results = [{"name": s.name, "url": s.get_absolute_url()} for s in services]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)



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
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_news') 
    else:
        form = NewsForm()

    return render(request, 'admin_pages/add_news.html', {'form': form})


@login_required(login_url='user_login')
def view_news(request):
    places = News.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_news.html', {'places': places})


@login_required(login_url='user_login')
def update_news(request, id):
    place = get_object_or_404(News, id=id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('view_news')
    else:
        form = NewsForm(instance=place)
    return render(request, 'admin_pages/update_news.html', {'form': form, 'place': place})

@login_required(login_url='user_login')
def delete_news(request,id):
    places = News.objects.get(id=id)
    places.delete()
    return redirect('view_news')

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
@login_required(login_url='user_login')
def view_menus(request):
    menus = Menu.objects.all()
    return render(request, "admin_pages/view_menus.html", {"menus": menus})

@login_required(login_url='user_login')
def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_menus')
    else:
        form = MenuForm()
    return render(request, 'admin_pages/add_menus.html', {'form': form})

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def delete_menu(request, pk):
    menu = get_object_or_404(Menu, id=pk)
    menu.delete()
    return redirect('view_menus')


# ----------------------------
# Category
# ----------------------------

# Add Category
@login_required(login_url='user_login')
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
@login_required(login_url='user_login')
def view_categories(request):
    categories = Category.objects.all().order_by('order')
    return render(request, "admin_pages/view_categories.html", {"categories": categories})

# Update Category
@login_required(login_url='user_login')
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
@login_required(login_url='user_login')
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect('view_categories')

# View all services
@login_required(login_url='user_login')
def view_services(request):
    services = Service.objects.all().order_by('-order')
    return render(request, 'admin_pages/view_services.html', {'services': services})


# Add service
@login_required(login_url='user_login')
def add_service(request):
    categories = Category.objects.all().order_by('menu', 'order')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()

            # Save dynamic process steps
            for key in request.POST:
                if key.startswith('new_step_title_'):
                    step_num = key.split('_')[-1]
                    title = request.POST.get(f'new_step_title_{step_num}')
                    description = request.POST.get(f'new_step_description_{step_num}')
                    if title and description:
                        ServiceProcessStep.objects.create(
                            service=service,
                            step_number=int(step_num),
                            title=title,
                            description=description
                        )

            # Save dynamic FAQs
            for key in request.POST:
                if key.startswith('new_faq_question_'):
                    faq_num = key.split('_')[-1]
                    question = request.POST.get(f'new_faq_question_{faq_num}')
                    answer = request.POST.get(f'new_faq_answer_{faq_num}')
                    if question and answer:
                        ServiceFAQ.objects.create(
                            service=service,
                            question=question,
                            answer=answer
                        )

            return redirect('view_services')
    else:
        form = ServiceForm()

    return render(request, 'admin_pages/add_service.html', {
        'form': form,
        'categories': categories
    })


# Update service
@login_required(login_url='user_login')
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    categories = Category.objects.all().order_by('menu', 'order')

    if request.method == 'POST':
        # Update main service info
        service.name = request.POST.get('name')
        service.slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        if category_id:
            service.category = get_object_or_404(Category, id=category_id)
        service.description = request.POST.get('description')

        # Update image if uploaded
        if 'image' in request.FILES:
            service.image = request.FILES['image']

        service.save()

        # Update existing steps
        existing_step_ids = [step.id for step in service.process_steps.all()]
        for step_id in existing_step_ids:
            step = service.process_steps.get(id=step_id)
            title = request.POST.get(f'step_title_{step.id}')
            description = request.POST.get(f'step_description_{step.id}')
            if title and description:
                step.title = title
                step.description = description
                step.save()
            else:
                step.delete()  # Delete if user removed content

        # Add new steps
        for key in request.POST:
            if key.startswith('new_step_title_'):
                step_num = int(key.split('_')[-1])
                title = request.POST.get(f'new_step_title_{step_num}')
                description = request.POST.get(f'new_step_description_{step_num}')
                if title and description:
                    ServiceProcessStep.objects.create(
                        service=service,
                        step_number=step_num,
                        title=title,
                        description=description
                    )

        # Update existing FAQs
        existing_faq_ids = [faq.id for faq in service.faqs.all()]
        for faq_id in existing_faq_ids:
            faq = service.faqs.get(id=faq_id)
            question = request.POST.get(f'faq_question_{faq.id}')
            answer = request.POST.get(f'faq_answer_{faq.id}')
            if question and answer:
                faq.question = question
                faq.answer = answer
                faq.save()
            else:
                faq.delete()  # Delete if user removed content

        # Add new FAQs
        for key in request.POST:
            if key.startswith('new_faq_question_'):
                faq_num = int(key.split('_')[-1])
                question = request.POST.get(f'new_faq_question_{faq_num}')
                answer = request.POST.get(f'new_faq_answer_{faq_num}')
                if question and answer:
                    ServiceFAQ.objects.create(
                        service=service,
                        question=question,
                        answer=answer
                    )

        return redirect('view_services')

    return render(request, 'admin_pages/update_service.html', {
        'service': service,
        'categories': categories
    })



# Delete service
@login_required(login_url='user_login')
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('view_services')


# --- Blog Categories ---
@login_required(login_url='user_login')
def add_blog_category(request):
    if request.method == "POST":
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_blog_categories')
    else:
        form = BlogCategoryForm()
    return render(request, 'admin_pages/add_blog_category.html', {'form': form})


@login_required(login_url='user_login')
def view_blog_categories(request):
    categories = BlogCategory.objects.all()
    return render(request, 'admin_pages/view_blog_category.html', {'categories': categories})


@login_required(login_url='user_login')
def update_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == "POST":
        form = BlogCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_blog_categories')
    else:
        form = BlogCategoryForm(instance=category)
    return render(request, 'admin_pages/update_blog_category.html', {'form': form})


@login_required(login_url='user_login')
def delete_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    category.delete()
    return redirect('view_blog_categories')


# --- Blogs ---
@login_required(login_url='user_login')
def add_blog(request):
    categories = BlogCategory.objects.all()  # Pass categories to template
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_blogs')
    else:
        form = BlogForm()
    
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'admin_pages/add_blogs.html', context)


@login_required(login_url='user_login')
def view_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'admin_pages/view_blogs.html', {'blogs': blogs})


@login_required(login_url='user_login')
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    categories = BlogCategory.objects.all()  # For the dropdown

    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        category_id = request.POST.get('category')
        blog.category = BlogCategory.objects.get(pk=category_id)

        # Handle image upload if a new image is selected
        if request.FILES.get('image'):
            blog.image = request.FILES['image']

        blog.save()
        return redirect('view_blogs')

    return render(request, 'admin_pages/update_blogs.html', {
        'blog': blog,
        'categories': categories
    })


@login_required(login_url='user_login')
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('view_blogs')