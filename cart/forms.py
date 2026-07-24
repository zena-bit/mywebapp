import re
from django import forms
from django.core.exceptions import ValidationError

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'})
    )
    last_name = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'})
    )
    company_name = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'company_name'})
    )
    address = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'House Number Street Name'})
    )
    city = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'city'})
    )
    country = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'country'})
    )
    postcode = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'postcode'})
    )
    mobile = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'mobile'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'order_notes', 'rows': 11, 'placeholder': 'Order Notes (Optional)'})
    )

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("First name can only contain letters, spaces, hyphens, and apostrophes.")
        if len(name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Last name can only contain letters, spaces, hyphens, and apostrophes.")
        if len(name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")
        return name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '').strip()
        # Allow leading + and digits only. E.g. +254123456789 or 0712345678
        cleaned_mobile = re.sub(r'[\s\-()]+', '', mobile) # strip spaces, hyphens, brackets
        if not re.match(r"^\+?\d{9,15}$", cleaned_mobile):
            raise ValidationError("Enter a valid phone number (e.g. +254123456789 or 0712345678), between 9 and 15 digits.")
        return cleaned_mobile

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", city):
            raise ValidationError("City name can only contain letters, spaces, hyphens, and apostrophes.")
        if len(city) < 2:
            raise ValidationError("City name must be at least 2 characters long.")
        return city

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", country):
            raise ValidationError("Country name can only contain letters, spaces, hyphens, and apostrophes.")
        if len(country) < 2:
            raise ValidationError("Country name must be at least 2 characters long.")
        return country
