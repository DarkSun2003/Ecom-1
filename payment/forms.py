from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    # Overriding fields to remove labels and add placeholders
    shipping_full_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
    required=True)
    shipping_email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
    required=True)
    shipping_address_line1 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
    required=True)
    shipping_address_line2 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
        required=False
    )
    shipping_city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
    required=True)
    shipping_state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=True
    )
    shipping_zipcode = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
        required=False
    )
    shipping_country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=True
    )
    
    class Meta:
        model = ShippingAddress
        # No need to list fields here if you have defined them above
        # The form will automatically use the fields you defined
        exclude = ('user',)
        
        
class PaymentForm(forms.Form):
    card_name = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name On Card'}), required=True)
    card_number = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required=True)
    card_exp_date = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exp Date'}), required=True)
    card_cvv_number = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}), required=True)
    card_address1 = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'}), required=True)
    card_address2 = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}), required=False)
    card_city = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing City'}), required=True)
    card_state =forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=True)
    card_zipcode = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}), required=False)
    card_country = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Country'}), required=True)