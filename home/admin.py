from django.contrib import admin

from home.models import ServiceType, Customer, ServicePage, Weddingbooking

admin.site.register(ServicePage)
admin.site.register(ServiceType)
admin.site.register(Customer)
admin.site.register(Weddingbooking)
