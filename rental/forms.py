from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Car, CustomUser, Rental


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["name", "brand", "model", "price", "available", "image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

class RentalCarForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['user', 'car']
