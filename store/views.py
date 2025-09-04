from sre_constants import CATEGORY
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


def search(request):
    """
    Handles the product search functionality.
    """
    if request.method == "POST":
        searched_term = request.POST.get('searched')

        # Check if the search term is empty or None
        if not searched_term:
            messages.info(request, "Please enter a search term.")
            return render(request, 'search.html', {})

        # Query the database using the search term
        searched_products = Product.objects.filter(
            Q(name__icontains=searched_term) | 
            Q(description__icontains=searched_term) | 
            Q(category__name__icontains=searched_term)
        ).distinct()
        
        # Check if the query returned any products
        if not searched_products:
            messages.info(request, f"No products matched your search for '{searched_term}'.")
            return render(request, 'search.html', {'searched_term': searched_term})
        
        # If products are found, render the page with the results
        return render(request, 'search.html', {
            'searched_term': searched_term, 
            'searched_products': searched_products
        })

    else:
        # For GET requests (initial page load)
        return render(request, 'search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        # Safely get or create the user's profile and shipping address
        try:
            current_user_profile = Profile.objects.get(user__id=request.user.id)
            shipping_user_address, created_shipping = ShippingAddress.objects.get_or_create(user__id=request.user.id)
        except Exception as e:
            messages.error(request, f"An error occurred: {e}. Please contact support.")
            return redirect('home')

        if request.method == "POST":
            # Pass the POST data and instances to the forms
            form = UserInfoForm(request.POST or None, instance=current_user_profile)
            shipping_form = ShippingForm(request.POST, instance=shipping_user_address)

            # Check if both forms are valid before saving
            if form.is_valid() and shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, "Your Info Has Been Updated Successfully.")
                return redirect('home')
            else:
                messages.error(request, "There was an error with your submission. Please check the form.")
        else:
            # For a GET request, create forms with existing data
            form = UserInfoForm(instance=current_user_profile)
            shipping_form = ShippingForm(instance=shipping_user_address)

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    
    else:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')




def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            #Do stuff
            form = ChangePasswordForm(current_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, ("You have updated your password successfully."))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, ("You must be logged in to view that page."))
        return redirect('home')
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("You have updated your profile successfully."))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, ("You must be logged in to view that page."))
        return redirect('home')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def category(request, category_name):
    #Grab the category from the url
    try:
        # look up category
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, "That category does not exist.")
        return redirect('home')
    
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #get their saved cart from db
            saved_cart = current_user.old_cart
            #convert database str to db dic
            if saved_cart:
                #convert to dic using JSON
                converted_cart = json.loads(saved_cart)
                #set the session cart to the converted cart
                #get the cart
                cart = Cart(request)
                #loop through the cart and add the item from the db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                
            
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.success(request, "Invalid username or password.")
            return redirect('login')
    else:    
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Been Registered Successfully, Please Create Profile."))
            return redirect('update_info')
        else:
            messages.success(request, ("Registration failed. There was a problem with your registration. Please try again."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
