from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


#Lets Mix Profile info and User info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend the User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name',]
    inlines = [ProfileInline]
#Unregister the original User admin    
admin.site.unregister(User)
#Re-register the new User admin
admin.site.register(User, UserAdmin)
# Register your models here.
