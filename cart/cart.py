from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request
        # get the current session key for the cart
        cart = self.session.get('session_key')
        
        # if the cart is not in the session, create it
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # make sure cart is available in all pages of site
        self.cart = cart
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # logic to add product to cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert{'3':4, '5':2} to {"3":4, "5":2}
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            #save carty to profile
            current_user.update(old_cart=carty)
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic to add product to cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert{'3':4, '5':2} to {"3":4, "5":2}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty to profile
            current_user.update(old_cart=carty)
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to look up products from database
        products = Product.objects.filter(id__in=product_ids)
        #return the looked up product
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #get the cart
        ourcart = self.cart
        #update dictionary/cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert{'3':4, '5':2} to {"3":4, "5":2}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty to profile
            current_user.update(old_cart=carty)
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        #delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert{'3':4, '5':2} to {"3":4, "5":2}
            carty = str(self.cart)
            carty = carty.replace("'", '"')
            #save carty to profile
            current_user.update(old_cart=carty)
        
    def cart_totals(self):
        #get product ids
        quantities = self.cart
        product_ids = self.cart.keys()
        #lookup products in database
        products = Product.objects.filter(id__in=product_ids)
        #start counting at 0
        total = 0
        for key, value in quantities.items():
            #convert key to int for calculations
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
        
        