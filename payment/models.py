from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.EmailField()
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=20, blank=True, null=True)
    shipping_country = models.CharField(max_length=100)
    
    #Dont Pluralize Address
    class Meta:
        verbose_name_plural = 'Shipping Address'


    def __str__(self):
        return f"Shipping Address - {str(self.id)}"
    
    
#Create a Shipping Address by default when a user  signs up    
def create_shipping(sender, instance, created, **kwargs):
    if created:
       user_shipping = ShippingAddress(user=instance)
       user_shipping.save()
       
#Automate the profile creation
post_save.connect(create_shipping, sender=User)

    
    
#Order Model

class Order(models.Model):
    #foreignkeys
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.DecimalField(max_digits=26, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order - {str(self.id)}"
    
#Auto add shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
    
#Order Item Model

class OrderItem(models.Model):
    #foreignkeys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null =True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null =True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=26, decimal_places=2)
    
    
    def __str__(self):
        return f"Order Item - {str(self.id)}"