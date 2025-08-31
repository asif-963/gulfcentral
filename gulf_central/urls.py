from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.index, name= 'index'),
    path('about/', views.about, name= 'about'),
    path('service-details/', views.service_details, name= 'service-details'),
    path('contact/', views.contact, name= 'contact'),

          # Admin Login
    path('login',views.user_login,name='user_login'),
    path('logout_user', views.logout_user, name='logout_user'),

    # admin dashboard
    path('dashboard',views.dashboard,name='dashboard'),

       # NEar By Place
    path('add_near_by_place', views.add_near_by_place, name='add_near_by_place'),
    path('view_near_by_place',views.view_near_by_place,name='view_near_by_place'),
    path('update_near_by_place/<int:id>/',views.update_near_by_place,name='update_near_by_place'),
    path('delete_near_by_place/<int:id>/',views.delete_near_by_place,name='delete_near_by_place'),

    path('ckeditor_upload/', views.ckeditor_upload, name='ckeditor_upload'),

    # client reviews
    path('add_client_review',views.add_client_review,name='add_client_review'),
    path('view_client_reviews',views.view_client_reviews,name='view_client_reviews'),
    path('update_client_review/<int:id>/',views.update_client_review,name='update_client_review'),
    path('delete_client_review/<int:id>/',views.delete_client_review,name='delete_client_review'),

    # Contact us
    path('contact_view',views.contact_view,name='contact_view'),
    path('delete_contact/<int:id>/',views.delete_contact,name='delete_contact'),

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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = 'gulf_central.views.page_404'