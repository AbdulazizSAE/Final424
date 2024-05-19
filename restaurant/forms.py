from django import forms
from .models import MenuItem

class UserForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)

class SignupForm(forms.Form):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'time_to_serve', 'description']
