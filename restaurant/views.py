from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MenuItem, Purchase
from .forms import UserForm, SignupForm, MenuItemForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "restaurant/menu.html", {"menu_items": menu_items})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("restaurant:menu"))
        else:
            return render(request, "restaurant/signup.html", {"form": form})
    return render(request, "restaurant/signup.html", {"form": SignupForm()})

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("restaurant:menu"))
            else:
                return render(request, "restaurant/login.html", {"form": form, "error": "Invalid credentials"})
        else:
            return render(request, "restaurant/login.html", {"form": form})
    return render(request, "restaurant/login.html", {"form": UserForm()})

@login_required
def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("restaurant:menu"))
    else:
        form = MenuItemForm()
    return render(request, "restaurant/add_menu_item.html", {"form": form})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        purchase, created = Purchase.objects.get_or_create(user=request.user, item=item)
        if not created:
            purchase.quantity += quantity
        purchase.save()
        return redirect('restaurant:item_detail', pk=pk)

    purchases = Purchase.objects.filter(item=item).select_related('user')
    return render(request, 'restaurant/item_detail.html', {
        'item': item,
        'purchases': purchases,
    })

@login_required
def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('restaurant:item_detail', pk=pk)
    else:
        form = MenuItemForm(instance=item)
    return render(request, "restaurant/item_form.html", {"form": form})