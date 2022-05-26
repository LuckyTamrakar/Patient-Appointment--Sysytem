from email.mime import image


from tokenize import Number
from unicodedata import name
from django import forms
from .models import john, Profile, phone_regex, riya, larry, james, himanshi, sohil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField



def email_exist(value):
    if User.objects.filter(email=value).exists():
        return forms.ValidationError("Profile with this Email Address already exists")

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[email_exist])
    name = forms.CharField(max_length = 20)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields  =['username','email']

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=17,validators=[phone_regex])
    
    
    class Meta:
        model = Profile
        fields = ['phone_number']

class John(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(validators=[email_exist])
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
	
	

    
    class Meta:
        model = john 
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']

class Riya(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
    time = forms.IntegerField(widget = forms.HiddenInput(), required = False)
	
	

    
    class Meta:
        model = riya 
        
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']
class Larry(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
	
	

    
    class Meta:
        model = larry 
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']

class James(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
	
	

    
    class Meta:
        model = james
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']

class Himanshi(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
	
	

    
    class Meta:
        model = himanshi 
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']

class Sohil(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=12)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    date = forms.CharField(max_length=10)
	
	

    
    class Meta:
        model = sohil
        fields = ['name', 'email', 'phone', 'city', 'address', 'date']

