from django.contrib import admin
from .models import  john, Profile, Contact, riya, james, himanshi, larry, sohil
# Register your models here.

from django.contrib.auth.models import User

@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','email_verified','uuid','name']
admin.site.register(Contact)
admin.site.register(john)
admin.site.register(riya)
admin.site.register(larry)
admin.site.register(james)
admin.site.register(himanshi)
admin.site.register(sohil)