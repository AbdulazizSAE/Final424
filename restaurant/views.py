from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenuItem
from .forms import UserForm, SignupForm, MenuItemForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password

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
                user = User.objects.create_user(
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
                if user.check_password(password):
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

def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'restaurant/item_detail.html', {'item': item})
