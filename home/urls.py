from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path('service_type/<int:type_id>/', views.service_type, name='service_type'),
    path('service/<uuid:service_id>/', views.service_detail, name='service_detail'),
    path('book_service/<uuid:booking_id>/', views.book_service, name='book_service'),
    path('charge/', views.charge, name='charge'),
    path('booking_confirmation/<uuid:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)