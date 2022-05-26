
from email.policy import default
from logging import debug
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid
# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class john(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

class riya(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

class larry(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

class james(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    time = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

class himanshi(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

class sohil(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time = models.IntegerField(max_length=10,default=0)
    date = models.CharField(max_length=50, default="")
    
    
    


    def __str__(self):
        return self.name

