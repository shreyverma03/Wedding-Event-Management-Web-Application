from django import forms
from django.forms import ModelForm, widgets
from .models import Customer, Weddingbooking, ServicePage


# from django.forms.widgets import DatePickerInput


class BookingForm(forms.ModelForm):
    class Meta:
        model = Weddingbooking
        fields = ['event_date', 'event_location', 'featured_package_price','service_page']

    # customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    # event_date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'))
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    event_location = forms.CharField(max_length=255)
    featured_package_price = forms.DecimalField(max_digits=10, decimal_places=2)

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        service_id = kwargs.pop('service_id')
        super().__init__(*args, **kwargs)
        service = ServicePage.objects.get(id=service_id)
        self.fields['featured_package_price'].initial = service.featured_package_price
        self.fields['featured_package_price'].widget.attrs['readonly'] = True
        self.fields['service_page'].initial = service.id
        self.fields['service_page'].widget.attrs['readonly'] = True
            #forms.ModelChoiceField(
            #queryset=ServicePage.objects.filter(id=service_id),
         #   widget=forms.HiddenInput()
        #)

    class Media:
        js = ['js/customer_autocomplete.js']
