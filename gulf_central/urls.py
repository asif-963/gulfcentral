from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.index, name= 'index'),
    path('about/', views.about, name= 'about'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('mainland-details/', views.mainland, name= 'mainland'),
    path('freezone-details/', views.freezone, name= 'freezone'),
    path('offshore-details/', views.offshore, name= 'offshore'),

    path('blogs/', views.blogs, name= 'blogs'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'), 


     path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('cost-calculator/', views.cost_calculator, name='cost_calculator'),



    path('service/<slug:slug>/', views.service_details, name='service_details'),

    path('contact/', views.contact, name= 'contact'),

    path('terms-and-conditions/', views.terms_and_conditions, name= 'terms-and-conditions'),
    path('privacy-and-policy/', views.privacy_and_policy, name= 'privacy-and-policy'),

     path('ajax/search-services/', views.ajax_search_services, name='ajax_search_services'),

          # Admin Login
    path('login',views.user_login,name='user_login'),
    path('logout_user', views.logout_user, name='logout_user'),

    # admin dashboard
    path('dashboard',views.dashboard,name='dashboard'),

       # NEar By Place
    path('add_news', views.add_news, name='add_news'),
    path('view_news',views.view_news,name='view_news'),
    path('update_news/<int:id>/',views.update_news,name='update_news'),
    path('delete_news/<int:id>/',views.delete_news,name='delete_news'),

    path('ckeditor_upload/', views.ckeditor_upload, name='ckeditor_upload'),

    # client reviews
    path('add_client_review',views.add_client_review,name='add_client_review'),
    path('view_client_reviews',views.view_client_reviews,name='view_client_reviews'),
    path('update_client_review/<int:id>/',views.update_client_review,name='update_client_review'),
    path('delete_client_review/<int:id>/',views.delete_client_review,name='delete_client_review'),

   

     # MENUS
    path('menus/', views.view_menus, name='view_menus'),
    path('menus/add/', views.add_menu, name='add_menu'),
    path('menus/update/<int:pk>/', views.update_menu, name='update_menu'),
    path('menus/delete/<int:pk>/', views.delete_menu, name='delete_menu'),

     # CATEGORY
    path('add-category/', views.add_category, name='add_category'),
    path('view-categories/', views.view_categories, name='view_categories'),
    path('update-category/<int:pk>/', views.update_category, name='update_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),

    # SERVICES
    path('services/', views.view_services, name='view_services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/update/<int:service_id>/', views.update_service, name='update_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),


    # --- Blog Categories ---
    path('blog-category/add/', views.add_blog_category, name='add_blog_category'),
    path('blog-category/view/', views.view_blog_categories, name='view_blog_categories'),
    path('blog-category/update/<int:pk>/', views.update_blog_category, name='update_blog_category'),
    path('blog-category/delete/<int:pk>/', views.delete_blog_category, name='delete_blog_category'),

    path('blogs/add/', views.add_blog, name='add_blog'),
    path('blogs/view/', views.view_blogs, name='view_blogs'),
    path('blogs/update/<int:pk>/', views.update_blog, name='update_blog'),
    path('blogs/delete/<int:pk>/', views.delete_blog, name='delete_blog'),

    path('add-pricing/', views.add_pricing_section, name='add_pricing'),
    path('view-pricing/', views.view_pricing_sections, name='view_pricing'),  # updated view function name
    path('update-pricing/<int:section_id>/', views.update_pricing_section, name='update_pricing'),
    path('delete-pricing/<int:section_id>/', views.delete_pricing_section, name='delete_pricing'),


   path('view-enquiries/', views.view_enquiries, name='view_enquiries'),
   path('enquiries/delete/<int:enquiry_id>/', views.delete_enquiry, name='delete_enquiry'),

     path('view-contacts/', views.view_contacts, name='view_contacts'),
    path('contacts/delete/<int:pk>/', views.delete_contact, name='delete_contact'),

    path('view-service-enquiries/', views.view_service_enquiries, name='view_service_enquiries'),
    path('service-enquiries/delete/<int:id>/', views.delete_service_enquiry, name='delete_service_enquiry'),

    path('teams/', views.view_teams, name='view_teams'),
    path('teams/add/', views.add_team, name='add_team'),
    path('teams/update/<int:pk>/', views.update_team, name='update_team'),
     path('teams/delete/<int:pk>/', views.delete_team, name='delete_team'),

    path('add-client-logo/', views.add_client_logo, name='add_client_logo'),
    path('view-client-logos/', views.view_client_logos, name='view_client_logos'),
    path('update-client-logo/<int:pk>/', views.update_client_logo, name='update_client_logo'),
    path('delete-client-logo/<int:pk>/', views.delete_client_logo, name='delete_client_logo'),




   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'gulf_central.views.page_404'