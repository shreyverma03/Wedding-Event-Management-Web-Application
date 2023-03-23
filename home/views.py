from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, request, JsonResponse
from .models import Weddingbooking
from django.urls import reverse
from django.core.mail import send_mail
import requests, stripe
from EventsForU import settings
from django.views.decorators.http import require_GET
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from_email = settings.EMAIL_HOST_USER

stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import ServicePage, ServiceType, Customer, Weddingbooking
YOUR_DOMAIN = 'http://127.0.0.1/8081'

def customer_autocomplete(request):
    query = request.GET.get('query', '')
    customers = Customer.objects.filter(
        name__icontains=query
    )[:10]
    results = [{'label': str(c), 'value': c.id} for c in customers]
    return JsonResponse({'results': results})


def index(request):
    services = ServicePage.objects.all()
    return render(request, 'index.html', {'services': services})


def service_type(request, type_id):
    service_type = get_object_or_404(ServiceType, pk=type_id)
    services = ServicePage.objects.filter(service_type=service_type)
    return render(request, 'service_type.html', {'service_type': service_type, 'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(ServicePage, pk=service_id)
    form = BookingForm(request.POST or None, service_id=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST or None, service_id=service_id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service_page = service

            customer = Customer.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone_number']
            )
            booking.customer = customer

            booking.save()

            return redirect('book_service', booking_id=booking.id)

    return render(request, 'service_detail.html', {'service': service, 'form': form})


def book_service(request, booking_id):
    # service = get_object_or_404(ServicePage, pk=service_id)
    print(booking_id)
    booking = get_object_or_404(Weddingbooking, pk=booking_id)
    return render(request, 'payment.html', {'booking_id': booking_id, 'booking': booking})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})


# def index(request):
#    events = EventPage.objects.all()
#    contact = Contact.objects.values()
#    return render(request, 'index.html', {'events': events, 'contact': contact})


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if username is not None and password is not None:
            if user is not None:
                auth.login(request, user)
                messages.info(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.info(request, "invalid credentials")
                return redirect('home')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':  # fetching the data from form
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already in use')
            return redirect('home')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already in use')
            return redirect('home')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname)
            user.save()
            messages.info(request, 'Successfully Registered. You can now login to your account.')
            return redirect('home')
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def charge(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        print("booking:",request.POST)
        booking = Weddingbooking.objects.get(id=booking_id)

        stripe_token = request.POST.get('stripeToken')
        print(stripe_token)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'product_data': {
                            'name': 'Service Booking',
                        },
                        'unit_amount': int(booking.featured_package_price * 100),
                    },
                    'quantity':1,

                }],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
            )

            booking.payment_status = True
            booking.save()
            messages.success(request,
                             f'Thank you for booking our {booking.service_page.title} Service !')
            return redirect('index')
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})


stripe.api_key = settings.STRIPE_SECRET_KEY
