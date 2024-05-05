from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from . models import STATUS_CHOICES, Coupon, Customer, Product, Category, OrderPlaced, ProductOffer

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput
    (attrs={'autofocus ':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput
    (attrs={'autocomplete ':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput
    (attrs={'autofocus ':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput
    (attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput
    (attrs={'class':'form-control' }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput
    (attrs={'class':'form-control' }))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs=
    {'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

#forgot password    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password",widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm New Password",widget=forms.PasswordInput(attrs=
    {'autocomplete':'current-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductIdForm(forms.Form):
    product_id = forms.IntegerField(label='Enter Product ID')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

#twilio
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))

#for email verification form
class SubscribeForm(forms.Form):
    email = forms.EmailField()

#cart management
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['status']

class EditOrderForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = OrderPlaced
        fields = ['status']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount', 'lower_limit', 'upper_limit', 'active']
        widgets = {
            'coupon_code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'lower_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'upper_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['product', 'discount_percentage']
        labels = {
            'product': 'Product',
            'discount_percentage': 'Discount Percentage',
        }