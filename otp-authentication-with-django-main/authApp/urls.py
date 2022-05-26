from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.home,name="home"),
    path('registration/',views.Registration, name="Registration"),
    path('registration/otp/',views.otpRegistration, name="otp-Registration"),
    path('login/',views.userLogin, name="user-login"),
    path('login/otp/',views.otpLogin, name="otp-login"),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html')),
    path('contact/', views.contact, name ='contact'),
    path('about/', views.About, name ='about'),
    path('image_upload', views.appointment1, name = 'image_upload'),
    
    path('appointment1/', views.appointment1, name ='appointment'),
    path('appointment2/', views.appointment2, name ='appointment1'),
    path('appointment3/', views.appointment3, name ='appointment2'),
    path('appointment4/', views.appointment4, name ='appointment3'),
    path('appointment5/', views.appointment5, name ='appointment4'),
    path('appointment6/', views.appointment6, name ='appointment5'),
    path('email-verify/', views.email_verification, name="email-verify"),
    path('forget-password/',views.forget_password,name="forger-password"),
    path('forget-password/done/',TemplateView.as_view(template_name='forget-password-done.html')),
    path('change-password/<slug:uid>/',views.change_password,name="change-password"),
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
