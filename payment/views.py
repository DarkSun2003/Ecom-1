from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime

# Create your views here.
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)
        #get the order items
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            #check if true or false
            if status =="True":
                #get the order
                order = Order.objects.filter(id=pk)
                #update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Order Status Updated")
            return redirect('home')
        
        return render(request, "payment/orders.html", {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            #grab datetime
            now = datetime.datetime.now()
            #update order
            order.update(shipped=False, date_shipped=now)
            messages.success(request, "Order Status Updated")
            return redirect('home')
        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
    messages.success(request, "Ordered placed")
    return redirect("home")

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            #grab datetime
            now = datetime.datetime.now()
            #update order
            order.update(shipped=True, date_shipped=now)
            
            messages.success(request, "Order Status Updated")
            return redirect('home')
        
        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")

def process_order(request):
    if request.POST:
        #get cart stuff
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()
            #Payment form
        payment_form = PaymentForm(request.POST or None)
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        #Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # lets create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address_line1']}\n{my_shipping['shipping_address_line2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        
        
        if request.user.is_authenticated:
            #logged in
            user = request.user
            #lets create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            #lets add order items
            # Lets get the Order ID
            order_id = create_order.pk
            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
             #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete key
                    del request.session[key]
            #delete from database (old cart view)
            current_user = Profile.objects.filter(user__id=request.user.id)
            #delete shopping cart in database(old cart view)
            current_user.update(old_cart="")
                    
            
            messages.success(request, "Ordered placed")
            return redirect("home")
        else:
            #not logged in
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
             #lets add order items
            # Lets get the Order ID
            order_id = create_order.pk
            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
            #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete key
                    del request.session[key]
            
            
            
            
            messages.success(request, "Ordered placed")
            return redirect("home")
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
        
def billing_info(request):
    if request.POST:
        
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_totals()
        #create a session for shipping info 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        #check to see if user is logged in
        if request.user.is_authenticated:
            #lets get the billing form
            billing_form = PaymentForm
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, 'billing_form':billing_form})
    else:
        messages.error(request, "Access Denied")
        return redirect("home")
        
def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_totals()
    
    if request.user.is_authenticated:
        #checkout as logged in user
        #Shipping User
        shipping_user_address= ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping form
        if request.method == "POST":
            shipping_form = ShippingForm(request.POST, instance=shipping_user_address)
            if shipping_form.is_valid():
                shipping_form.save()
                return redirect("checkout")
        else:
            shipping_form = ShippingForm(instance=shipping_user_address)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    
    else:
        #checkout as guest
        shipping_form = ShippingForm(request.POST)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
