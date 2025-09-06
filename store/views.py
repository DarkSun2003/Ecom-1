from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.

def home(request):
    """
    Displays the home page with all products.
    """
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    """
    Displays the about page.
    """
    return render(request, 'about.html', {})

def login_user(request):
    """
    Handles user login and cart restoration.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                current_user = Profile.objects.get(user=request.user)
                saved_cart = current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
            except Profile.DoesNotExist:
                pass # User might not have a profile yet
            except json.JSONDecodeError:
                messages.error(request, "Error restoring your cart.")
            
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    """
    Logs out the current user.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register_user(request):
    """
    Handles new user registration.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered successfully! Please create your profile."))
            return redirect('update_info')
        else:
            messages.error(request, "Registration failed. Please try again.")
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

def product(request, pk):
    """
    Displays the details of a single product.
    """
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, category_name):
    """
    Displays all products for a specific category.
    """
    try:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "That category does not exist.")
        return redirect('home')

def category_summary(request):
    """
    Displays a list of all product categories.
    """
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def update_user(request):
    """
    Allows the user to update their username and email.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')
    
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)
    if user_form.is_valid():
        user_form.save()
        login(request, current_user)
        messages.success(request, "You have updated your profile successfully.")
        return redirect('home')
    return render(request, 'update_user.html', {'user_form': user_form})

def update_password(request):
    """
    Allows the user to change their password.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('home')

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated your password successfully.")
            login(request, request.user)
            return redirect('update_user')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('update_password')
    else:
        form = ChangePasswordForm(request.user)
        return render(request, 'update_password.html', {'form': form})
    
def update_info(request):
    """
    Allows the user to update their profile and shipping information.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')

    try:
        current_user_profile, created_profile = Profile.objects.get_or_create(user=request.user)
        shipping_user_address, created_shipping = ShippingAddress.objects.get_or_create(user=request.user)
    except Exception as e:
        messages.error(request, f"An error occurred: {e}. Please contact support.")
        return redirect('home')

    if request.method == "POST":
        form = UserInfoForm(request.POST or None, instance=current_user_profile)
        shipping_form = ShippingForm(request.POST, instance=shipping_user_address)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your info has been updated successfully.")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = UserInfoForm(instance=current_user_profile)
        shipping_form = ShippingForm(instance=shipping_user_address)

    return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})

def search(request):
    """
    Handles the product search functionality.
    """
    if request.method == "POST":
        searched_term = request.POST.get('searched')
        if not searched_term:
            messages.info(request, "Please enter a search term.")
            return render(request, 'search.html', {})

        searched_products = Product.objects.filter(
            Q(name__icontains=searched_term) | 
            Q(description__icontains=searched_term) | 
            Q(category__name__icontains=searched_term)
        ).distinct()
        
        if not searched_products:
            messages.info(request, f"No products matched your search for '{searched_term}'.")
            return render(request, 'search.html', {'searched_term': searched_term})
        
        return render(request, 'search.html', {
            'searched_term': searched_term, 
            'searched_products': searched_products
        })
    else:
        return render(request, 'search.html', {})
