import re
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileForm, John, Riya, Larry, James, Himanshi, Sohil
from .models import Profile, Contact, john, riya, james, larry, himanshi, sohil, User
import requests
from random import randint
from django.contrib.auth.hashers import make_password
import random
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
# Create your views here.

def About(request):
    return render(request, 'about.html')
def send_otp(number,message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    api = "qzeoVJBgIOrA1w78WPkS6EX02ZTQi9NtLyuva3Cl4nFjsKHdmfYpQ8ELiUs2hVmegqKDFxI5u1dcOXzl"
    querystring = {"authorization":api,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":number}
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)

    


def Registration(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            n = fm.cleaned_data['name']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            message = f'your wecare Login otp is {otp}'
            send_otp(p_number,message)
            return redirect('/registration/otp/')

    else:
        fm  = UserRegistrationForm()
        up = UserProfileForm()
    context = {'fm':fm,'up':up}
    return render(request,'registration.html',context)


def otpRegistration(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session['username']
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email') 

        if int(u_otp) == otp:
            User.objects.create(
                            username = user,
                            email=email_address,
                            password=hash_pwd
            )
            user_instance = User.objects.get(username=user)
            Profile.objects.create(
                            user = user_instance,phone_number=p_number
            )
            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('phone_number')

            messages.success(request,'Registration Successfully Done !!')

            return redirect('/login/')
        
        else:
            messages.error(request,'Wrong OTP')


    return render(request,'registration-otp.html')


def userLogin(request):

    try :
        if request.session.get('failed') > 2:
            return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    except:
        request.session['failed'] = 0
        request.session.set_expiry(100)



    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            u = User.objects.get(username=username)
            p = Profile.objects.get(user=u)
            p_number = p.phone_number
            otp = random.randint(1000,9999)
            request.session['login_otp'] = otp
            message = f'your otp of Wecare is {otp}'
            send_otp(p_number,message)
            return redirect('/login/otp/')
        else:
            messages.error(request,'username or password is wrong')
    return render(request,'login.html')

def otpLogin(request):
    if request.method == "POST":
        username = request.session['username']
        password = request.session['password']
        otp = request.session.get('login_otp')
        u_otp = request.POST['otp']
        if int(u_otp) == otp:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                request.session.delete('login_otp')
                messages.success(request,'login successfully')
                return redirect('/')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'login-otp.html')

def home(request):
    if request.method == "POST":
        otp = random.randint(1000,9999)
        request.session['email_otp'] = otp
        message = f'your Wecare login otp is {otp}'
        user_email = request.user.email

        send_mail(
            'Email Verification OTP',
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        return redirect('/email-verify/')

    return render(request,'home.html')

def email_verification(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session['email_otp']
        if int(u_otp) == otp:
           p =  Profile.objects.get(user=request.user)
           p.email_verified = True
           p.save()
           messages.success(request,f'Your email {request.user.email} is verified now')
           return redirect('/')
        else:
            messages.error(request,'Wrong OTP')


    return render(request,'email-verified.html')

def forget_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            url = f'http://127.0.0.1:8000/change-password/{uid.profile.uuid}'
            send_mail(
            'Reset Password',
            url,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
            return redirect('/forget-password/done/')
        else:
            messages.error(request,'email address is not exist')
    return render(request,'forget-password.html')

def change_password(request,uid):
    try:
        if Profile.objects.filter(uuid = uid).exists():
            if request.method == "POST":
                pass1 = 'password1'in request.POST and request.POST['password1']
                pass2 =  'password2'in request.POST and request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(uuid=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(request,'Password has been reset successfully')
                    return redirect('/login/')
                else:
                    return HttpResponse('Two Password did not match')
                
        else:
            return HttpResponse('Wrong URL')
    except:
        return HttpResponse('Wrong URL')
    return render(request,'change-password.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        htmly = get_template('Email.html')
        d = { 'name': name, 'email': email, 'address': address, 'phone': phone}
        subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        contact = Contact(name=name, email=email, phone=phone, desc=desc, address=address, city=city, state=state)
        contact.save()
    return render(request, 'contact.html')

def appointment1(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
       
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        if john.objects.filter(email=email).exists()  or john.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                    
                    
            app = john(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
                    
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
        
    return render(request, 'appointment2.html')

def appointment2(request):
    
    
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        
            
        if riya.objects.filter(email=email).exists()  or riya.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():   
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                
                
            app = riya(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
    return render(request, 'appointment2.html')        
      
def appointment3(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        if larry.objects.filter(email=email).exists()  or larry.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():
            
            
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                
                
            app = larry(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
    return render(request, 'appointment2.html')

def appointment4(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        if james.objects.filter(email=email).exists()  or james.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():
            
            
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                
                
            app = james(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
    return render(request, 'appointment2.html')

def appointment5(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        if himanshi.objects.filter(email=email).exists()  or himanshi.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():
            
            
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                
                
            app = himanshi(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
    return render(request, 'appointment2.html')

def appointment6(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        
        date = request.POST.get('date', '')
        time = random.randint(12,20)
        if sohil.objects.filter(email=email).exists()  or sohil.objects.filter(phone=phone).exists():
            return HttpResponse("Please use  another Email or Mobile number beacuse it already exists")   
        elif Profile.objects.filter(phone_number = phone).exists():
            
            
            htmly = get_template('Email.html')
            d = { 'name': name, 'date': date, 'email': email, 'address': address, 'phone': phone, 'time': time }
            subject, from_email, to = 'Thankyou for Appointment on Wecare', 'wecareclinic.02@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
                
                
            app = sohil(name=name, email=email, phone=phone, date=date, address=address, city=city, time = time)    
            app.save()
            return redirect('/')
        else:
            return HttpResponse("Please provide correct Detail")
    return render(request, 'appointment2.html')	

