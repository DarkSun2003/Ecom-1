from .cart import Cart

# Create a context processor to add the cart to all pages of the site
def cart(request):
    # return the default data from the Cart class
    return {'cart': Cart(request)}