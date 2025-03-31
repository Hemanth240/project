from django import forms
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth.forms import UserCreationForm


# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']

# User Registration Form
class RegistrationForm(forms.Form):  # ✅ Use `forms.Form`
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data
