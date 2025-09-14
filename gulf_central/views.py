from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import random

from .models import Menu, Category, Service, News, ClientReview, ServiceProcessStep, ServiceFAQ, BlogCategory, Blog, PricingSection, PricingPlan, PlanFeature
from .forms import NewsForm, MenuForm, CategoryForm, ServiceForm, ClientReviewForm, BlogCategoryForm, BlogForm
from .forms import ContactForm, ServiceEnquiryForm, TeamForm, ClientLogoForm
from .models import Contact, ServiceEnquiry, Team, ClientLogo












def index(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    client_reviews = ClientReview.objects.all()
    teams = Team.objects.all() 
    clients = ClientLogo.objects.all() 
    section = PricingSection.objects.prefetch_related("plans__features").first()
    latest_news = News.objects.order_by('-created_date')[:3]
    services = Service.objects.values_list('name', flat=True) 
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer))) 
    categories = list(Category.objects.prefetch_related('services').all())
    random.shuffle(categories)       # Shuffle all categories
    categories = categories[:6]   
    return render(request, 'index.html', {'menus': menus, 'client_reviews':client_reviews, 'teams':teams, 'clients': clients, 'latest_news':latest_news, 'categories': categories,'service_footer':random_services,'services':list(services), 'section':section})


def about(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    client_reviews = ClientReview.objects.all()
    teams = Team.objects.all()  
    clients = ClientLogo.objects.all() 
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    return render(request, 'about.html',{'menus': menus, 'client_reviews':client_reviews, 'clients': clients, 'teams':teams, 'service_footer':random_services})


# News listing page
def news(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    news_items = News.objects.order_by('-created_date')  # Latest news first
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    context = {'menus': menus, 'news_items': news_items, 'service_footer':random_services}
    return render(request, 'news.html', context)

# News details page
def news_detail(request, pk):
    menus = Menu.objects.prefetch_related('categories__services').all()
    news_item = get_object_or_404(News, pk=pk)
    latest_news = News.objects.exclude(pk=pk).order_by('-created_date')[:5]
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    context = {'news': news_item, 'menus': menus, 'latest_news':latest_news, 'service_footer':random_services}
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
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))

    return render(request, "blogs.html", {
        "menus": menus,
        "blogs": blogs,
        "categories": categories,
        "query": query,
        'service_footer':random_services
    })
def blog_detail(request, pk):
    menus = Menu.objects.prefetch_related('categories__services').all()
    blog = get_object_or_404(Blog, pk=pk)
    latest_blogs = Blog.objects.exclude(pk=pk)[:3]  # 3 latest posts excluding current
    categories = BlogCategory.objects.all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    
    return render(request, "blog-details.html", {
        "menus": menus,
        "blog": blog,
        "latest_blogs": latest_blogs,
        "categories": categories,
        'service_footer':random_services
    })



from .models import CostCalculatorEnquiry

def cost_calculator(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    return render(request, "cost-calculator.html", {
        "menus": menus,'service_footer':random_services })

from django.contrib import messages

def submit_enquiry(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)  # 👈 Add this for debugging

        CostCalculatorEnquiry.objects.create(
            business_activity=request.POST.get('business_activity'),
            jurisdiction=request.POST.get('jurisdiction'),
            sponsorship=request.POST.get('sponsorship', ''),
            owners=request.POST.get('owners'),
            visas=request.POST.get('visas'),
            office_required=request.POST.get('office_required'),
            company_name=request.POST.get('company_name', ''),
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            nationality=request.POST.get('nationality'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Enquiry submitted successfully!")
        return redirect('cost_calculator')
    return redirect('cost_calculator')





def mainland(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('mainland')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'mainland-details.html',{'form': form, 'menus': menus,'service_footer':random_services})

def freezone(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('freezone')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'freezone-details.html',{'form': form, 'menus': menus,'service_footer':random_services})

def offshore(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('offshore')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'offshore-details.html',{'form': form, 'menus': menus,'service_footer':random_services})

def service_details(request, slug):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.filter(category=service.category).exclude(id=service.id)
    process_steps = ServiceProcessStep.objects.filter(service=service).order_by('step_number')
    faqs = ServiceFAQ.objects.filter(service=service)
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))

    if request.method == 'POST':
        form = ServiceEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your enquiry has been submitted successfully!")
            return redirect(request.path_info)  # reload the same page to show toast
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceEnquiryForm(initial={'service_name': service.name})


    context = {
        'service': service,
        'process_steps': process_steps,
        'faqs': faqs,
        'related_services': related_services,
        'menus': menus,
        'form': form,
        'service_footer':random_services
    }

    return render(request, 'service-details.html', context)




def terms_and_conditions(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    return render(request, 'terms_and_conditions.html',{'menus': menus,'service_footer':random_services})

def privacy_and_policy(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    return render(request, 'privacy_and_policy.html',{'menus': menus,'service_footer':random_services})


def contact(request):
    menus = Menu.objects.prefetch_related('categories__services').all()
    service_footer = list(Service.objects.values('name', 'slug'))
    random_services = random.sample(service_footer, min(4, len(service_footer)))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'menus': menus,'service_footer':random_services})






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
            return redirect('add_category')
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
            return redirect('add_category')
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
            return redirect('add_service')
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
            return redirect('add_service')
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
            return redirect('add_blog')
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
            return redirect('add_blog')
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

from django.shortcuts import render, redirect, get_object_or_404
from .models import PricingSection, PricingPlan, PlanFeature

# Add Pricing Section
@login_required(login_url='user_login')
def add_pricing_section(request):
    if request.method == "POST":
        # Create Section
        title = request.POST.get('section_title', '').strip()
        description = request.POST.get('section_description', '').strip()
        if title:
            section = PricingSection.objects.create(title=title, description=description)

            # Handle dynamic plans
            for key in request.POST:
                if key.startswith('plans[') and key.endswith('][title]'):
                    index = key.split('[')[1].split(']')[0]
                    plan_title = request.POST.get(f'plans[{index}][title]', '').strip()
                    plan_description = request.POST.get(f'plans[{index}][description]', '').strip()
                    if plan_title:
                        plan = PricingPlan.objects.create(section=section, title=plan_title, description=plan_description)

                        # Features for the plan
                        features = request.POST.getlist(f'plans[{index}][features][]')
                        for feature_text in features:
                            if feature_text.strip():
                                PlanFeature.objects.create(plan=plan, text=feature_text.strip())

            return redirect('view_pricing')

    return render(request, 'admin_pages/add_card.html')

# View all Pricing Sections
@login_required(login_url='user_login')
def view_pricing_sections(request):
    sections = PricingSection.objects.all()
    return render(request, 'admin_pages/view_card.html', {'sections': sections})

@login_required(login_url='user_login')
def update_pricing_section(request, section_id):
    section = get_object_or_404(PricingSection, id=section_id)

    if request.method == "POST":
        # update section
        section.title = request.POST.get("section_title")
        section.description = request.POST.get("section_description")
        section.save()

        # handle existing plans
        for plan in section.plans.all():
            keep_plan = request.POST.get(f"keep_plan_{plan.id}", "1")
            if keep_plan == "0":
                plan.delete()
                continue

            # update plan fields
            plan.title = request.POST.get(f"plan_title_{plan.id}", plan.title)
            plan.description = request.POST.get(f"plan_desc_{plan.id}", plan.description)
            plan.save()

            # handle features
            for feature in plan.features.all():
                keep_feature = request.POST.get(f"keep_feature_{feature.id}", "1")
                if keep_feature == "0":
                    feature.delete()
                    continue

                feature.text = request.POST.get(f"feature_{feature.id}", feature.text)
                feature.save()

            # new features
            for key, value in request.POST.items():
                if key.startswith(f"new_feature_{plan.id}_") and value.strip():
                    plan.features.create(text=value.strip())

        # handle new plans
        new_plan_titles = [k for k in request.POST if k.startswith("new_plan_title_")]
        for key in new_plan_titles:
            index = key.split("_")[-1]
            title = request.POST.get(f"new_plan_title_{index}")
            desc = request.POST.get(f"new_plan_desc_{index}")
            if title.strip():
                new_plan = section.plans.create(title=title.strip(), description=desc.strip())
                # add features
                for fk, fv in request.POST.items():
                    if fk.startswith(f"new_feature_plan_{index}_") and fv.strip():
                        new_plan.features.create(text=fv.strip())

        return redirect("view_pricing")

    return render(request, "admin_pages/update_card.html", {"section": section})


@login_required(login_url='user_login')
def delete_pricing_section(request, section_id):
    section = get_object_or_404(PricingSection, id=section_id)
    section.delete()
    return redirect('view_pricing')

@login_required(login_url='user_login')
def view_enquiries(request):
    enquiries = CostCalculatorEnquiry.objects.all().order_by('-created_at')
    return render(request, 'admin_pages/view_cost_calculator_enquiries.html', {'enquiries': enquiries})

@login_required(login_url='user_login')
def delete_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(CostCalculatorEnquiry, id=enquiry_id)
    enquiry.delete()
    messages.success(request, "Enquiry deleted successfully!")
    return redirect('view_enquiries')



@login_required(login_url='user_login')
def view_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin_pages/view_contacts.html', {'contacts': contacts})

@login_required(login_url='user_login')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Contact deleted successfully!")
    return redirect('view_contacts')


@login_required(login_url='user_login')
def view_service_enquiries(request):
    enquiries = ServiceEnquiry.objects.all().order_by('-created_at')
    return render(request, 'admin_pages/view_service_enquiries.html', {'enquiries': enquiries})

@login_required(login_url='user_login')
def delete_service_enquiry(request, id):
    enquiry = get_object_or_404(ServiceEnquiry, id=id)
    enquiry.delete()
    messages.success(request, "Service enquiry deleted successfully.")
    return redirect('view_service_enquiries')


def view_teams(request):
    teams = Team.objects.all()
    return render(request, 'admin_pages/view_teams.html', {'teams': teams})

def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_teams')
    else:
        form = TeamForm()
    return render(request, 'admin_pages/add_team.html', {'form': form})

def update_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('view_teams')
    else:
        form = TeamForm(instance=team)
    return render(request, 'admin_pages/update_team.html', {'form': form, 'team': team})

# Delete team member
def delete_team(request, pk):
    member = get_object_or_404(Team, pk=pk)
    member.delete()
    return redirect('view_teams')


# Client Logo
# Add Client Logo
def add_client_logo(request):
    if request.method == 'POST':
        form = ClientLogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_client_logos')
    else:
        form = ClientLogoForm()
    return render(request, 'admin_pages/add_client_logo.html', {'form': form})

# View All Client Logos
def view_client_logos(request):
    clients = ClientLogo.objects.all()
    return render(request, 'admin_pages/view_client_logos.html', {'clients': clients})

# Update Client Logo
def update_client_logo(request, pk):
    client = get_object_or_404(ClientLogo, pk=pk)
    if request.method == 'POST':
        form = ClientLogoForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('view_client_logos')
    else:
        form = ClientLogoForm(instance=client)
    return render(request, 'admin_pages/update_client_logo.html', {'form': form})

# Delete Client Logo
def delete_client_logo(request, pk):
    client = get_object_or_404(ClientLogo, pk=pk)
    client.delete()
    return redirect('view_client_logos')