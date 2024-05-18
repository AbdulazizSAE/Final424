from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import User, MenuItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

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

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "restaurant/menu.html", {"menu_items": menu_items})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            hashed_password = make_password(password)
            
            try:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=hashed_password
                )
                return HttpResponseRedirect(reverse("restaurant:menu"))
            except:
                return render(request, "restaurant/signup.html", {"form": form, "error": "Username or email already exists"})
        else:
            return render(request, "restaurant/signup.html", {"form": form})
    return render(request, "restaurant/signup.html", {"form": SignupForm()})

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    return HttpResponseRedirect(reverse("restaurant:menu"))
                else:
                    return render(request, "restaurant/login.html", {"form": form, "error": "Invalid credentials"})
            except ObjectDoesNotExist:
                return render(request, "restaurant/login.html", {"form": form, "error": "Invalid credentials."})
        else:
            return render(request, "restaurant/login.html", {"form": form})
    return render(request, "restaurant/login.html", {"form": UserForm()})

def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("restaurant:menu"))
    else:
        form = MenuItemForm()
    return render(request, "restaurant/add_menu_item.html", {"form": form})

#new 
def item_update(request, pk):
    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return render(request, "restaurant/error.html", {"message": "Item not found"})

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("restaurant:menu"))
    else:
        form = MenuItemForm(instance=item)
    return render(request, "restaurant/item_form.html", {"form": form})